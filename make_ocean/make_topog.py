import numpy as np
import netCDF4 as nc
import xarray as xr
import xesmf as xe

oceanfile = 'ocean_hgrid.nc'
topogfile = 'reconstruction_a1_0.25_degree.nc'
outfile = 'topog_49ka_conserv.nc'

f = nc.Dataset(oceanfile,'r')
oc_x = f.variables['x'][:]
oc_y = f.variables['y'][:]
f.close()

f = nc.Dataset(topogfile,'r')
topo = f.variables['paleo_topography'][11,:,:]
lat = f.variables['lat'][:]
lon = f.variables['lon'][:]
f.close()

topo = topo.astype('f8')

lon2d, lat2d = np.meshgrid(lon, lat)

lat_c = 0.5 * (lat[1:] + lat[:-1])
lon_c = 0.5 * (lon[1:] + lon[:-1])

lon2d_c, lat2d_c = np.meshgrid(lon_c, lat_c)

old_grid = xr.Dataset(coords={
    "lon": (("y","x"), lon2d),
    "lat": (("y","x"), lat2d)
    })

new_grid = xr.Dataset(coords={
    "lon": (("y","x"), lon2d_c),
    "lat": (("y","x"), lat2d_c),
    "lon_b": (("y_b","x_b"), lon2d),
    "lat_b": (("y_b","x_b"), lat2d)
    })

regrid_center = xe.Regridder(old_grid, new_grid, method="bilinear")

topo_c = regrid_center(topo.data)
topo_c = -1. * topo_c

oc_grid = xr.Dataset(coords={
    "lon": (("y","x"), oc_x[1::2,1::2]),
    "lat": (("y","x"), oc_y[1::2,1::2]),
    "lon_b": (("y_b","x_b"), oc_x[0::2,0::2]),
    "lat_b": (("y_b","x_b"), oc_y[0::2,0::2])  
    })

regridder = xe.Regridder(new_grid, oc_grid, method="conservative_normed")

topo_oc = regridder(topo_c)
topo_oc[topo_oc < 0.] = 0.

ds_o = xr.Dataset(coords={
    "lon": (("y","x"), oc_x[1::2,1::2]),
    "lat": (("y","x"), oc_y[1::2,1::2])    
    },
    data_vars={
    "depth": (("y","x"), topo_oc)
    })
ds_o.attrs['history'] = 'make_topog.py on %s' % topogfile
ds_o.to_netcdf(outfile)