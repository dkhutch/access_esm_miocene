import numpy as np
import xarray as xr

infile = 'topog_mio_atmos.nc'
lsmfile = 'lsm_mio_v3.nc'
outfile = 'topog_mio_atmos_antarc.nc'

ds_in = xr.open_dataset(infile)
topo = ds_in['topo'].data
lat = ds_in['lat'].data
lon = ds_in['lon'].data

ds_lsm = xr.open_dataset(lsmfile)
lsm = ds_lsm['lsm'].data

ny, nx = topo.shape

# First, flatten out the bottom three rows of latitude, else we have polar gradient problems:
topo[:3,:] = np.mean(topo[:3,:])

nxpad = 11
nxpad2 = int((nxpad - 1)/2)
nypad = 5
nypad2 = int((nypad - 1)/2)
nylim = 9


topo_pad = np.zeros((ny, nx+nxpad-1))
topo_pad[:,nxpad2:-nxpad2] = topo
topo_pad[:,:nxpad2] = topo[:,-nxpad2:]
topo_pad[:,-nxpad2:] = topo[:,:nxpad2]

topo_out = np.zeros((ny, nx))

for j in range(nylim):
    j0 = max(0, j - nypad2)
    j1 = j + nypad2
    for i in range(nx):
        topo_out[j,i] = np.mean(topo_pad[j0:j1, i:i+nxpad])

topo_out[nylim:,:] = topo[nylim:,:]
topo_out[lsm==0] = 0.

ds_o = xr.Dataset(coords={
    "lat": ("lat", lat[:,0]),
    "lon": ("lon", lon[0,:])
    },
    data_vars={
    "topo" : (("lat","lon"), topo_out)
    })
ds_o.lat.attrs['units'] = 'degrees_north'
ds_o.lon.attrs['units'] = 'degrees_east'
ds_o.attrs['history'] = f'smooth_antarc.py on {infile} \n'
ds_o.to_netcdf(outfile)