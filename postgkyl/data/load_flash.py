import numpy as np
import math
import tables as tbl
import os.path

def load_flash(file_name : str, var_name : str) -> tuple:
  fh = tbl.open_file(file_name, 'r')
  coord = fh.root['coordinates'].read().transpose()
  bsize = fh.root['block size'].read().transpose()
  ntype = fh.root['node type'].read().transpose()
  bdata = fh.root[var_name].read().transpose()

  nxb, nyb, _, N = bdata.shape
  res = bsize.min(axis=1)
  lower = (coord-bsize/2).min(axis=1)
  upper = (coord+bsize/2).max(axis=1)

  nxax = math.floor((upper[0]-lower[0]) / (res[0]/nxb))
  nyax = math.floor((upper[1]-lower[1]) / (res[1]/nyb))
  data = np.zeros((nxax, nyax))
  for b in range(N):
    if ntype[b] == 1:
      mult = np.ceil(bsize[:,b]/res)
      idxx = math.floor((coord[0,b] - bsize[0,b]/2 - lower[0]) / res[0] * nxb)
      idxy = math.floor((coord[1,b] - bsize[1,b]/2 - lower[1]) / res[1] * nyb)
      for i in range(nxb):
        for j in range(nyb):
          data[idxx+i*int(mult[0]):idxx+(i+1)*int(mult[0])+1,
               idxy+j*int(mult[1]):idxy+(j+1)*int(mult[1])+1] = bdata[i,j,0,b]
        #end
      #end
    #end
  #end
  fh.close()
  return 2, (nxax, nyax), (lower[:2], upper[:2]), data
#end