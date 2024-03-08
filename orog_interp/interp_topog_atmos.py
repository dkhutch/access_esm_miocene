import numpy as np
import netCDF4 as nc
import xarray as xr
import xesmf as xe

atmosfile = 'grids.nc'
miofile = 'miocene_topo_pollard_antscape_dolan_0.5x0.5.nc'
outfile = 'topog_mio_atmos.nc'
lsmfile = 'lsm_mio_v3.nc'
gridsavefile = 'grids_xesmf.nc'

f = nc.Dataset(atmosfile,'r')
at_x = f.variables['um1t.lon'][:]
at_y = f.variables['um1t.lat'][:]
at_xc = f.variables['um1t.clo'][:]
at_yc = f.variables['um1t.cla'][:]
f.close()

f = nc.Dataset(miofile,'r')
topo = f.variables['topo'][:]
lat = f.variables['lat'][:]
lon = f.variables['lon'][:]
f.close()

f = nc.Dataset(lsmfile,'r')
lsm = f.variables['lsm'][:]
f.close()

nlat, nlon = at_x.shape

xb = np.zeros((nlat+1, nlon+1), 'f8')
yb = np.zeros((nlat+1, nlon+1), 'f8')

xb[:-1,:-1] = at_xc[0,:,:]
xb[1:,1:] = at_xc[2,:,:]
xb[0,-1] = at_xc[1,0,-1]
xb[-1,0] = at_xc[3,-1,0]

yb[:-1,:-1] = at_yc[0,:,:]
yb[1:,1:] = at_yc[2,:,:]
yb[0,-1] = at_yc[1,0,-1]
yb[-1,0] = at_yc[3,-1,0]

topo = topo.astype('f8')

grid_mio = xe.util.grid_global(0.5, 0.5, lon1=359.75)
grid_mio["topo"] = (("y","x"), topo)

at_grid = xr.Dataset(coords={
    "lon": (("y","x"), at_x),
    "lat": (("y","x"), at_y),
    "lon_b": (("y_b","x_b"), xb),
    "lat_b": (("y_b","x_b"), yb)  
    })

at_grid.to_netcdf(gridsavefile)

regridder = xe.Regridder(grid_mio, at_grid, method="conservative_normed")

d_in = grid_mio["topo"]
topo_at = regridder(d_in)
topo_at = topo_at.rename("topo")
topo_at = topo_at.where(topo_at > 0, 0.)
topo_at = topo_at.where(lsm == 1, 0.)

topo_bot = np.mean(topo_at[0,:])
topo_at[0,:] = topo_bot

# topo_left = np.reshape(topo_at[:,-1], (nlat,1))
topo_left = topo_at[:,-1]
topo_left = np.reshape(topo_left.data, (nlat,1))
topo_right = topo_at[:,0]
topo_right = np.reshape(topo_right.data, (nlat,1))

topo_pad = np.concatenate((topo_left, topo_at, topo_right), axis=1)
topo_new = np.zeros((nlat, nlon), 'f8')

for i in range(1,nlon+1):
    i0 = i-1
    i1 = i+2
    for j in range(1,nlat-1):
        topo_new[j,i-1] = np.mean(topo_pad[j-1:j+2, i0:i1])

topo_new[0,:] = topo_at[0,:]
topo_new[-1,:] = topo_at[-1,:]
topo_at[:] = topo_new[:]

ds_o = xr.Dataset()
ds_o['topo'] = topo_at
ds_o.attrs['history'] = 'interp_topog_atmos.py'
ds_o.to_netcdf(outfile)
