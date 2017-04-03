import numpy as np
import os
import h5py
import argparse

parser = argparse.ArgumentParser(description='create computational domain to meep(refractive index map).Positions and sizes in micro meters.')
parser.add_argument('--LX', dest='LX', default=20.0, help='comp. domain X size', type=float)
parser.add_argument('--LY', dest='LY', default=20.0, help='comp. domain Y size', type=float)
parser.add_argument('--n_low', dest='n_low', default=1.44, help='Low refractive index', type=float)
parser.add_argument('--n_high', dest='n_high', default=3.45, help='High refractive index', type=float)
parser.add_argument('-r', dest='resolution', default=0.050, help='resolution', type=float)
parser.add_argument('--in_wv', dest='in_wv', default=True, help='Creates Input Waveguide if True', type=float)
parser.add_argument('--x_in', dest='x_in', default=0.0, help='Input wg X position (left corner)', type=float)
parser.add_argument('--y_in', dest='y_in', default=9.5, help='Input wg Y position (botton corner)', type=float)
parser.add_argument('--lx_in', dest='lx_in', default=10.0, help='Input wg X length', type=float)
parser.add_argument('--ly_in', dest='ly_in', default=0.450, help='Input wg Y length', type=float)
parser.add_argument('--out_wv', dest='out_wv', default=True, help='Creates Output Waveguide if True', type=float)
parser.add_argument('--x_out', dest='x_out', default=10.0, help='Output wg X position (left corner)', type=float)
parser.add_argument('--y_out', dest='y_out', default=9.5, help='Output wg Y position (botton corner)', type=float)
parser.add_argument('--lx_out', dest='lx_out', default=10.0, help='Output wg X length', type=float)
parser.add_argument('--ly_out', dest='ly_out', default=0.450, help='Output wg Y length', type=float)
parser.add_argument('--dev', dest='dev', default=True, help='Creates Device if True', type=float)
parser.add_argument('--x_dev', dest='x_dev', default=7.5, help='Device X position (left corner)', type=float)
parser.add_argument('--y_dev', dest='y_dev', default=7.5, help='Device Y position (botton corner)', type=float)
parser.add_argument('--lx_dev', dest='lx_dev', default=5.0, help='Device X length', type=float)
parser.add_argument('--ly_dev', dest='ly_dev', default=5.0, help='Device Y length', type=float)
parser.add_argument('-i', dest='device_file', default='device.csv', help='CVS file mapping the device refractive index')
parser.add_argument('-o', dest='index_file', default='index.h5', help='H5 file mapping full domain the refractive index')

parser.parse_args()
input = parser.parse_args()


LX=input.LX
LY=input.LY
n_low=input.n_low
n_high=input.n_high
resolution=input.resolution
x_in=input.x_in
y_in=input.y_in
lx_in=input.lx_in
ly_in=input.ly_in
x_out= input.x_out
y_out= input.y_out
lx_out=input.lx_out
ly_out=input.ly_out
x_dev= input.x_dev
y_dev= input.y_dev
lx_dev=input.lx_dev
ly_dev=input.ly_dev
in_wv=input.in_wv
out_wv=input.out_wv
dev=input.dev

device_file=input.device_file
index_file=input.index_file

subarray = np.genfromtxt(device_file, delimiter=',')
if np.array_equal(subarray.shape, np.array([lx_dev/resolution,lx_dev/resolution])):
  print "Device array matches"
else:  
  print "Device Array size " + str(subarray.shape) + " do not match the given length and resolution ratio " + str(np.array([lx_dev/resolution,lx_dev/resolution]))  
  #exit(1)  

def rf2i(x):
    global resolution
    return int(round(x/resolution))

domain = np.full( ( rf2i(LX) , rf2i(LY) ),n_low)

def block(x,y,lx,ly,n):
    global domain
    x=rf2i(x)
    lx=rf2i(lx)
    y=rf2i(y)
    ly=rf2i(ly)
    domain[x:x+lx ,y:y+ly] = n 

#Waveguide input
if in_wv:
   block(x_in,y_in,lx_in,ly_in,n_high)
#Waveguide output
if out_wv:
   block(x_out,y_out,lx_out,ly_out,n_high)
#Device
if dev:
   block(x_dev,y_dev,lx_dev,ly_dev,subarray)
    
h5f = h5py.File(index_file, 'w')
h5f.create_dataset('index', data=domain)
h5f.close()