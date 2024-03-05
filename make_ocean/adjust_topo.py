import numpy as np
import netCDF4 as nc
import os

infile = 'topog_49ka_conserv.nc'
outfile = 'topog_49ka.nc'
straitfile = 'straits.txt'

if not os.path.exists(outfile):
    cmd = f'cp {infile} {outfile}'
    os.system(cmd)

f = nc.Dataset(outfile,'r+')
f.history = 'adjust_topo.py on %s \n' % infile
f.title = outfile

if 'ntiles' not in f.dimensions:
    f.createDimension('ntiles',1)

depth = f.variables['depth']

data = depth[:]
ny, nx = data.shape

data[data < 20.] = 0.

min_depth = 40.
shallow = np.logical_and(data > 0., data < min_depth)
data[shallow] = min_depth

fill = np.zeros((ny,nx), 'bool')
dig = np.zeros((ny,nx), 'bool')

fill[0,:] = True

#------------------------------------
# INSERT FILL AND DIG BELOW THIS LINE
#------------------------------------


dig[202:204, 274] = True # Mediterranean open

#------------------------------------
# INSERT FILL AND DIG ABOVE THIS LINE
#------------------------------------

data[fill] = 0.
data[dig] = min_depth


depth0 = np.reshape(data[:,-1], (ny, 1))
depth1 = np.reshape(data[:,0], (ny, 1))
depth_pad = np.concatenate((depth0, data, depth1), axis=1)

straits = np.zeros((ny,nx+2), 'i4')
straits[depth_pad == 0] = 0
straits[depth_pad > 0] = 1

fs = open(straitfile,'w')

for j in range(1,ny-1):
    for i in range(1,nx):
        if depth_pad[j,i] > 0:
            upper = depth_pad[j+1,i] == 0
            lower = depth_pad[j-1,i] == 0
            right = depth_pad[j,i+1] == 0
            left = depth_pad[j,i-1] == 0

            if ((upper and lower) or (right and left)):
                straits[j,i] = 2
                fs.write('fill[%d, %d] = True\n' % (j, i-1))

fs.close()

depth[:] = data[:]
f.close()