import numpy as np
import os
from create_geo import *
from functions_simples import *

stdout = []
m = 51
n = 51
c = (np.random.rand(m,n) - 0.5) * 2

z = cebv2d_simples(100j,100j,c)

create_geo(in_wv=False,dev=False, lx_out=20, index_file='out_wg.h5')
create_geo(device_file='dev.csv', index_file='coupler.h5')

cmd = 'meep  template-meep.ctl'
stdout.append(os.popen(cmd).read())

cmd = 'meep index_file="coupler.h5" field_file_append="dev" template-meep.ctl'
stdout.append(os.popen(cmd).read())

f1 = fft2d_simples('template-meep-no-dev',0.6451612903225805,0.025) 
f2 = fft2d_simples('template-meep-dev',0.6451612903225805,0.025)
eff = overlap_simples(f1,f2,0.05,0.05)


#################################################################################
# plots -> time domain, frequency domain in the middle, mode at desired frequency
#################################################################################
pts_spa = np.linspace(1,len(f1[0]),len(f1[0]))
fig, ax = plt.subplots(4, 1)
ax[0].plot(pts_spa,np.abs(f1[0]),'r',pts_spa,np.abs(f2[0]),'b') # plotting the spectrum
ax[1].plot(pts_spa,np.abs(f1[1]),'r',pts_spa,np.abs(f2[1]),'b') # plotting the spectrum
ax[2].plot(pts_spa,np.abs(f1[2]),'r',pts_spa,np.abs(f2[2]),'b') # plotting the spectrum
ax[3].plot(pts_spa,np.abs(f1[3]),'b',pts_spa,np.abs(f2[3]),'b') # plotting the spectrum
plt.figure()
plt.imshow(z)
    
plt.show()
