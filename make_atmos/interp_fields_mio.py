import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import iris, umfile
from um_fileheaders import *
from stashvar import atm_stashvar
import os
import xesmf as xe
import xarray as xr

restartfile = 'restart.subset'
new_restart = 'restart.mio'
lsm_pi_file = 'lsm_esm1.5.nc'
lsm_mio_file = 'lsm_mio_v3.nc'
maskvar = 'lsm'
netcdf_landfrac = 'landfrac_um1t.nc'
mask_file = 'masks.nc'
mask_file_orig = 'masks_orig.nc'


f = nc.Dataset(lsm_pi_file, 'r')
lsm_pi = f.variables['lsm'][:]
f.close()
lsm_pi = lsm_pi.astype('i4')

f = nc.Dataset(lsm_mio_file, 'r')
lsm_mio = f.variables['lsm'][:]
lat = f.variables['latitude'][:]
lon = f.variables['longitude'][:]
f.close()
lsm_mio = lsm_mio.astype('i4')

nlat, nlon = lsm_pi.shape

f = nc.Dataset(mask_file,'r')
at_mask_cpl = f.variables['um1t.msk'][:]
f.close()

f = nc.Dataset(mask_file_orig,'r')
at_mask_cpl_orig = f.variables['um1t.msk'][:]
f.close()

f = nc.Dataset(netcdf_landfrac,'r')
landfrac_new = f.variables['landfrac'][:]
f.close()

new_ocean = np.logical_and(lsm_pi==1, lsm_mio==0)
new_land = np.logical_and(lsm_pi==0, lsm_mio==1)
land_pts = lsm_mio==1

seaice = at_mask_cpl==0
no_seaice = at_mask_cpl==1

lon_m, lat_m = np.meshgrid(lon, lat)

# Set up regridder for nearest neighbour interpolations:
old_grid = xr.Dataset(coords={
    "lon": (("y","x"), lon_m),
    "lat": (("y","x"), lat_m)},
    data_vars={
    "mask": (("y","x"), lsm_pi)
    })

new_grid = xr.Dataset(coords={
    "lon": (("y","x"), lon_m),
    "lat": (("y","x"), lat_m)
    })

regridder = xe.Regridder(old_grid, new_grid, method='nearest_s2d')

os.system('cp {} {}'.format(restartfile, new_restart))
os.system('um_replace_field.py -v 30 -n {} -V {} {}'.format(
    lsm_mio_file, maskvar, new_restart))

fin = umfile.UMFile(restartfile, 'r')
f = umfile.UMFile(new_restart, 'r+')
nvars = f.fixhd[FH_LookupSize2]

lsm_code = 30
landfrac_code = 505
snow_codes = [23, 95, 416]
ice_reset = [49, 415]
ice_zeros = [31, 32, 413, 414, 416, 509]
ice_temp = 508
oc_curr = [28, 29, 269, 270]

# orog_vars = [17, 18, 33, 34, 35, 36, 37]

for k in range(nvars):
    ilookup = fin.ilookup[k]
    lbegin = ilookup[LBEGIN] 
    if lbegin == -99:
        break
    a = fin.readfld(k)

    if ilookup[ITEM_CODE] in oc_curr:
        a[:] = 0.
    if a.shape == (nlat, nlon):
        if ilookup[ITEM_CODE] == lsm_code:
            continue
        elif ilookup[ITEM_CODE] == landfrac_code:
            a[:] = landfrac_new[:]
        elif ilookup[ITEM_CODE] in snow_codes:
            a[:] = 0.
        elif ilookup[ITEM_CODE] in ice_zeros:
            a[:] = 0.
        elif ilookup[ITEM_CODE] in ice_reset:
            a[seaice] = ice_reset_val
            a[no_seaice] = fin.missval_r
        elif ilookup[ITEM_CODE] == ice_temp:
            a[:] = ice_reset_val
        elif ilookup[ITEM_CODE] == 33:
            a_new = regridder(a)
            a[new_land] = a_new[new_land]
            a[new_ocean] = 0.
        elif ilookup[LBPACK]==120:
            a_new = regridder(a)
            a[new_land] = a_new[new_land]
            a[new_ocean] = fin.missval_r
    f.writefld(a[:], k)
f.close()

