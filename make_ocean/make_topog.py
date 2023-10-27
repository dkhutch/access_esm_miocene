import numpy as np
import netCDF4 as nc
import xarray as xr
import xesmf as xe

oceanfile = 'ocean_hgrid.nc'
miofile = 'miocene_topo_pollard_antscape_dolan_0.5x0.5.nc'
outfile = 'topog_mio_conserv.nc'

f = nc.Dataset(oceanfile,'r')
oc_x = f.variables['x'][:]
oc_y = f.variables['y'][:]
f.close()

f = nc.Dataset(miofile,'r')
topo = f.variables['topo'][:]
lat = f.variables['lat'][:]
lon = f.variables['lon'][:]
f.close()

topo = topo.astype('f8')

grid_mio = xe.util.grid_global(0.5, 0.5, lon1=359.75)
grid_mio["depth"] = (("y","x"), -1.0 * topo)

oc_grid = xr.Dataset(coords={
    "lon": (("y","x"), oc_x[1::2,1::2]),
    "lat": (("y","x"), oc_y[1::2,1::2]),
    "lon_b": (("y_b","x_b"), oc_x[0::2,0::2]),
    "lat_b": (("y_b","x_b"), oc_y[0::2,0::2])  
    })

regridder = xe.Regridder(grid_mio, oc_grid, method="conservative_normed")

d_in = grid_mio["depth"]
topo_oc = regridder(d_in)
topo_oc = topo_oc.rename("depth")
topo_oc = topo_oc.where(topo_oc > 0, 0.)

topo_oc.to_netcdf(outfile)