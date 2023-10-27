import numpy as np
import netCDF4 as nc
import os

infile = 'kmt_dp.nc'
outfile = 'kmt.nc'
topofile = 'topog_mio_v3.nc'

os.system('cp {} {}'.format(infile, outfile))
os.system('chmod ug+w {}'.format(outfile))

f = nc.Dataset(topofile, 'r')
topo = f.variables['depth'][:]
f.close()

f = nc.Dataset(outfile, 'r+')
f.history = 'fix_kmt.py \n'
f.title = 'kmt_mio_v3.nc'

kmt = f.variables['kmt']
data = kmt[:]
data[topo==0] = 0
data[topo>0] = 1
kmt[:] = data[:]

f.close()