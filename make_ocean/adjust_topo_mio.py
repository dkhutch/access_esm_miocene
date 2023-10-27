import numpy as np
import netCDF4 as nc
import os

infile = 'topog_mio_conserv.nc'
outfile = 'topog_mio_v3.nc'
straitfile = 'straits.txt'

if not os.path.exists(outfile):
    cmd = f'cp {infile} {outfile}'
    os.system(cmd)

f = nc.Dataset(outfile,'r+')
f.history = 'adjust_topo_mio.py on %s \n' % infile
f.title = outfile

if 'ntiles' not in f.dimensions:
    f.createDimension('ntiles',1)

depth = f.variables['depth']

data = depth[:]
ny, nx = data.shape

min_depth = 40.
shallow = np.logical_and(data > 0., data < min_depth)
data[shallow] = min_depth

fill = np.zeros((ny,nx), 'bool')
dig = np.zeros((ny,nx), 'bool')

fill[0,:] = True
fill[1, 163] = True
fill[1, 196] = True
fill[1, 198] = True
fill[1, 199] = True
fill[1, 200] = True
fill[1, 201] = True
fill[1, 202] = True
fill[2, 195] = True
fill[3, 195] = True
fill[6, 65] = True
fill[6, 163] = True
fill[7, 65] = True
fill[9, 191] = True
fill[10, 168] = True
fill[11, 66] = True
fill[11, 162] = True
fill[11, 164] = True
fill[11, 202] = True
fill[12, 186] = True
fill[13, 64] = True
fill[13, 151] = True
fill[14, 64] = True
fill[14, 153] = True
fill[15, 32] = True
fill[15, 64] = True
fill[15, 67] = True
fill[15, 68] = True
fill[18, 27] = True
fill[18, 77] = True
fill[20, 29] = True
fill[21, 72] = True
fill[21, 279] = True
fill[22, 64] = True
fill[23, 293] = True
fill[23, 299] = True
fill[24, 81] = True
fill[25, 65] = True
fill[26, 347] = True
fill[27, 57] = True
fill[27, 211] = True
fill[28, 56] = True
fill[29, 2] = True
fill[29, 4] = True
fill[30, 7] = True
fill[30, 62] = True
fill[30, 215] = True
fill[32, 59] = True
fill[52, 208] = True
fill[57, 208] = True
fill[58, 65] = True
fill[60, 97] = True
fill[60, 208] = True
fill[61, 209] = True
fill[64, 59] = True
fill[65, 54] = True
fill[76, 226] = True
fill[82, 39] = True
fill[85, 312] = True
fill[102, 50] = True
fill[104, 51] = True
fill[121, 28] = True
fill[121, 237] = True
fill[122, 240] = True
fill[124, 202] = True
fill[133, 287] = True
fill[140, 35] = True
fill[142, 28] = True
fill[147, 273] = True
fill[160, 198] = True
fill[162, 216] = True
fill[164, 211] = True
fill[164, 214] = True
fill[175, 23] = True
fill[178, 18] = True
fill[179, 18] = True
fill[180, 18] = True
fill[182, 348] = True
fill[183, 348] = True
fill[184, 13] = True
fill[187, 345] = True
fill[191, 31] = True
fill[193, 37] = True
fill[194, 38] = True
fill[196, 333] = True
fill[197, 194] = True
fill[198, 191] = True
fill[198, 293] = True
fill[199, 326] = True
fill[200, 192] = True
fill[200, 329] = True
fill[204, 329] = True
fill[205, 305] = True
fill[205, 328] = True
fill[206, 304] = True
fill[206, 326] = True
fill[208, 332] = True
fill[209, 289] = True
fill[210, 304] = True
fill[212, 291] = True
fill[213, 292] = True
fill[216, 217] = True
fill[216, 218] = True
fill[216, 219] = True
fill[217, 278] = True
fill[218, 272] = True
fill[220, 267] = True
fill[221, 59] = True
fill[222, 59] = True
fill[223, 271] = True
fill[225, 153] = True
fill[231, 124] = True
fill[233, 82] = True
fill[233, 128] = True
fill[234, 126] = True
fill[236, 131] = True
fill[237, 132] = True
fill[238, 118] = True
fill[238, 138] = True
fill[239, 118] = True
fill[240, 82] = True
fill[241, 83] = True
fill[244, 102] = True
fill[244, 115] = True
fill[245, 102] = True
fill[246, 102] = True
fill[247, 102] = True
fill[248, 106] = True
fill[249, 106] = True
fill[256, 117] = True
fill[257, 63] = True
fill[257, 82] = True
fill[259, 92] = True
fill[260, 95] = True
fill[260, 102] = True
fill[264, 132] = True
fill[265, 149] = True
fill[269, 191] = True
fill[269, 202] = True
fill[270, 191] = True
fill[272, 157] = True
fill[273, 42] = True
fill[273, 156] = True
fill[275, 40] = True
fill[277, 196] = True
fill[278, 266] = True
fill[279, 213] = True
fill[280, 168] = True
fill[281, 32] = True
fill[282, 33] = True
fill[282, 216] = True
fill[282, 249] = True
fill[284, 165] = True
fill[284, 218] = True
fill[285, 223] = True
fill[285, 224] = True
fill[286, 202] = True
fill[286, 215] = True
fill[287, 156] = True
fill[287, 205] = True
fill[288, 44] = True
fill[288, 150] = True
fill[288, 171] = True
fill[289, 312] = True
fill[290, 234] = True
fill[293, 168] = True
fill[294, 174] = True
fill[295, 173] = True
fill[296, 170] = True
fill[296, 175] = True
fill[296, 210] = True
fill[297, 175] = True
fill[297, 304] = True
fill[298, 197] = True
fill[298, 198] = True
fill[298, 199] = True
fill[298, 200] = True
fill[298, 209] = True

fill[1, 195] = True
fill[5, 163] = True
fill[10, 164] = True
fill[19, 27] = True
fill[20, 28] = True
fill[27, 56] = True
fill[62, 209] = True
fill[199, 191] = True
fill[199, 192] = True
fill[199, 327] = True
fill[201, 329] = True
fill[224, 271] = True
fill[260, 101] = True
fill[275, 41] = True
fill[282, 32] = True
fill[287, 157] = True
fill[290, 235] = True
fill[295, 174] = True
fill[298, 210] = True
fill[19, 28] = True
fill[198, 327] = True
fill[201, 328] = True
fill[198, 328] = True

fill[13:24, 29:35] = True
fill[4:13, 64:69] = True
fill[25:30, 18:30] = True
fill[63:67, 60:64] = True
fill[23:28, 54:59] = True
fill[23:25, 64:66] = True

dig[206, 42] = True
dig[212, 222] = True
dig[283, 201] = True
dig[284, 202] = True
dig[195, 329] = True
dig[18, 348] = True
dig[9, 167] = True
dig[8, 190] = True
dig[212, 295:297] = True
dig[209:212, 304] = True
dig[211, 305] = True
dig[212, 305:307] = True
dig[205:207, 325] = True
dig[206, 324] = True
dig[285, 202] = True
dig[298, 146:150] = True
dig[299, 209] = True
dig[298, 209:214] = True
dig[281, 36] = True
dig[287, 214] = True
dig[212, 334] = True
dig[284, 157] = True
dig[219, 272] = True
dig[57, 95] = True
dig[62, 95] = True

fill[297:300, 170:173] = True

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