import numpy as np
import netCDF4 as nc

infile = 'landfrac_um1t.nc'
outfile = 'lsm_mio_v3.nc'

f = nc.Dataset(infile,'r')
lat = f.variables['latitude'][:]
lon = f.variables['longitude'][:]
landfrac = f.variables['landfrac'][:]
f.close()

nlat, nlon = landfrac.shape

lsm = np.copy(landfrac)
lsm[lsm >= 0.01] = 1.


f = nc.Dataset(outfile,'w')
f.history = f'mask_lsm.py on {infile} \n'

f.createDimension('latitude', nlat)
f.createDimension('longitude', nlon)

lat_o = f.createVariable('latitude','f8', ('latitude'))
lat_o.units = 'degrees_north'
lat_o[:] = lat[:]

lon_o = f.createVariable('longitude', 'f8', ('longitude'))
lon_o.units = 'degrees_east'
lon_o[:] = lon[:]

lsm_o = f.createVariable('lsm', 'f8', ('latitude','longitude'))
lsm_o.units = 'binary land-sea mask'
lsm_o[:] = lsm[:]

f.close()