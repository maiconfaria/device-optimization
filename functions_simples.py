import numpy as np
import h5py
import matplotlib.pylab as plt
#import matplotlib.pylab as plt

def fft2d_simples(file_name,
                  freq, 
                  dt):
    '''
    Function to calculate the fft for fields in .h5 format.
    meep 2d simulation.
    Time fields in a single vector (monitor 1d).
    
    file_name              : .h5 file name
    freq                   : desired frequency in meep units
    dt                     : resolution time in meep units
    
    Return 'fields_freq' = [Ex,Ey,Ez,Hx,H1,Hz] -> fields in the frequency domain'      
    '''
    ####################################
    # Read the fields in the time domain
    #################################### 
    h5f = h5py.File('/home/jlan13/ownCloud/pita-stuff/'+ file_name +'.h5','r')
    ex1 = np.complex128(np.array(h5f["ex"])) 
    ey1 = np.complex128(np.array(h5f["ey"]))
    ez1 = np.complex128(np.array(h5f["ez"]))
    hx1 = np.complex128(np.array(h5f["hx"]))
    hy1 = np.complex128(np.array(h5f["hy"]))
    hz1 = np.complex128(np.array(h5f["hz"]))
    h5f.close() 
    #print ex1.shape 
    ############################
    # Data for the fft form meep
    ############################
    pts = len(ex1[0,:])             # points of f(t) 
    Fs = 1/dt                       
    L = dt*pts                     # simulation time
    n = pts
    #t = np.linspace(0, L, pts)     # time vector
    
    #####################################
    # fields in the frquency domain - fft
    #####################################
    cont = 0
    nfft = 2**16                               # For zero padding
    al = np.complex128([ex1,ey1,hx1,hy1])      # All fields in the time domain
    ex1f = np.zeros((len(ex1[:,0]),nfft))
    ey1f = np.zeros((len(ex1[:,0]),nfft))
    ez1f = np.zeros((len(ex1[:,0]),nfft))
    hx1f = np.zeros((len(ex1[:,0]),nfft))
    hy1f = np.zeros((len(ex1[:,0]),nfft))
    hz1f = np.zeros((len(ex1[:,0]),nfft))
    als = [ex1f,ey1f,ez1f,hx1f,hy1f,hz1f]
                                  
    for aux in al:
        for i in range(len(ex1[:,0])):
            als[cont][i,:] = np.fft.fft(aux[i,:],n=nfft)/n
        cont += 1
    #print als
    #########################################
    # Take the filed in the desired frequency
    #########################################
    #freq = 0.6451612903225805                     # Desired Frequency
    nfreq = np.int(np.round(nfft*freq/Fs,0))       # Position f the desired frequency
    xf = np.linspace(-nfft/2,nfft/2,nfft)*Fs/nfft  # frequency vector
    Ex1 = als[0][:,nfft/2+nfreq]
    Ey1 = als[1][:,nfft/2+nfreq]
    Ez1 = als[2][:,nfft/2+nfreq]
    Hx1 = als[3][:,nfft/2+nfreq]
    Hy1 = als[4][:,nfft/2+nfreq]
    Hz1 = als[5][:,nfft/2+nfreq]
    pts_fre = np.linspace(1,len(Ex1),len(Ex1))      # Spatial vector
    fields_freq = [Ex1,Ey1,Ez1,Hx1,Hy1,Hz1]
    # write fields as dataset in a .h5
    #h5w = h5py.File('/home/jlan13/ownCloud/pita-stuff/fields_freq.h5', 'w')
    #h5w.create_dataset('Exf', data=Ex1)
    #h5w.close()

    return fields_freq

'''
#################################################################################
# plots -> time domain, frequency domain in the middle, mode at desired frequency
#################################################################################
fig, ax = plt.subplots(3, 1)
ax[0].plot(t,al[0][101,:])
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Amplitude')
ax[1].plot(xf[nfft/2:], als[0][101,nfft/2:],'r') # plotting the spectrum
ax[1].set_xlabel('Freq (Hz)')
ax[1].set_ylabel('|Y(freq)|')
ax[2].plot(pts_fre,np.abs(als[0]),'k') # plotting the spectrum
    
plt.show()
'''

##################    
# overlap integral 
##################

def overlap_simples(fields1,
                    fields2,
                    dx,
                    dy):
    '''
    Function to calculate the overlap integral.
    All imput fields must have the same grid.
    
    fields1                   : fields in frequency 1
    fields2                   : fields in frequency 2
    dx                        : spatial resolution in x
    dy                        : spatial resolution in y
    
    Return  'n' coupling efficiency.      
    '''
    # FIELD IN THE DESIRED FREQUENCY
    Ex1 = fields1[0]
    Ey1 = fields1[1]
    Ez1 = fields1[2]
    Hx1 = fields1[3]
    Hy1 = fields1[4]
    Hz1 = fields1[5]
    s1 = Ex1*(Hy1.conjugate())-Ey1*(Hx1.conjugate())
    s1_int = 0.5*sum(s1.real*dx)
    #s1_int = 0.5*sum(sum((s1.real)*dx*dy))
    print s1_int
    #print s1.shape,s1_int
    
    # FILED NORMALIZED WITH THE POITNITNG VECTOR 
    Ex1_n = Ex1/np.sqrt(s1_int)
    Ey1_n = Ey1/np.sqrt(s1_int)
    Hx1_n = Hx1/np.sqrt(s1_int)
    Hy1_n = Hy1/np.sqrt(s1_int)
    s1_n = Ex1_n*Hy1_n.conjugate()-Ey1_n*Hx1_n.conjugate()
    s1_int_n = 0.5*sum(s1_n.real*dx)
    #s1_int_n = 0.5*sum(sum(s1_n.real*dx*dy))
    print s1_int_n
    
    # FIELD IN THE DESIRED FREQUENCY
    Ex2 = fields2[0]
    Ey2 = fields2[1]
    Ez2 = fields2[2]
    Hx2 = fields2[3]
    Hy2 = fields2[4]
    Hz2 = fields2[5]
    
    s2 = Ex2*(Hy2.conjugate())-Ey2*(Hx2.conjugate())
    s2_int = 0.5*sum(s2.real*dx)
    #s2_int = 0.5*sum(sum((s2.real)*dx*dy))
    print s2_int
    #print s1.shape,s1_int
    
    # FILED NORMALIZED WITH THE POITNITNG VECTOR 
    Ex2_n = Ex2/np.sqrt(s2_int)
    Ey2_n = Ey2/np.sqrt(s2_int)
    Hx2_n = Hx2/np.sqrt(s2_int)
    Hy2_n = Hy2/np.sqrt(s2_int)
    
    s2_n = Ex2_n*Hy2_n.conjugate()-Ey2_n*Hx2_n.conjugate()
    s2_int_n = 0.5*sum(s2_n.real*dx)
    #s2_int_n = 0.5*sum(sum(s2_n.real*dx*dy))
    print s1_int_n
     
    # Coupling calculation
    
    c = sum(0.5*((Ex1_n*Hy2_n.conjugate()-Ey1_n*Hx2_n.conjugate())))*dx
    #c = sum(sum(0.5*((Ex1_n*Hy2_n.conjugate()-Ey1_n*Hx2_n.conjugate()))))*dx*dy
    n = 20*np.log10(abs(c))
    
    print "coupling efficiency:", n
    print ("%.15f" % n )
    return n

def cebv2d_simples(x,
                   y,
                   c):
    '''
    Evaluate a 2-D Chebyshev series at points (x, y).
    
    x                             : array_like The two dimensional series is evaluated at the points (x, y),
    y                             : where x and y must have the same shape 
    c                             : Array of coefficients ordered                                
    
    Returns: 'z' The values of the two dimensional Chebyshev series at points 
    formed from pairs of corresponding values from x and y.
    '''
    m = 32
    n = 32
    y,x = np.mgrid[-1:1:x,-1:1:y] 
    #print("DoF's: " + str(m*n))
    z = np.polynomial.chebyshev.chebval2d(x,y,c)
    for n in np.nditer(z, op_flags=['readwrite']):
        if n < 0:
            n[...] = 1.45
        else:
            n[...] = 3.45
    np.savetxt("dev.csv", z,fmt='%10.2f', delimiter=",")

    return z 