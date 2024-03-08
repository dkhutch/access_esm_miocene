import numpy as np
import xarray as xr
from scipy.stats import linregress

stddev_file = 'herold_etal_stddev_subgrid_etopo1_to_eocene_1x1.nc'
paleo_topo = 'topog_mio_atmos_antarc.nc'
outfile = 'stddev_mio.nc'

ds = xr.open_dataset(stddev_file)
std_av = ds['mean_of_stddev']
ht_av = ds['mean_of_heights']

cutoff = 30
ht_cutoff = 3000

r1 = linregress(ht_av[:cutoff], std_av[:cutoff])
r2 = linregress(ht_av[cutoff:], std_av[cutoff:])


ds_t = xr.open_dataset(paleo_topo)
topo = ds_t['topo']
new_std = topo.where(topo >= ht_cutoff, topo * r1.slope + r1.intercept)
new_std = new_std.where(topo < ht_cutoff, topo * r2.slope + r2.intercept)
new_std = new_std.where(topo > 0, np.nan)

ds_o = xr.Dataset()
ds_o['stddev'] = new_std
ds_o.attrs['history'] = 'remake_stddev.py'
ds_o.to_netcdf(outfile)

''' From NCL script... strange values I can't understand!! 
rc1 = 0.05800274
intercept1 = 153.1946

rc2 = 0.06556392
intercept2 = 42.53493
'''