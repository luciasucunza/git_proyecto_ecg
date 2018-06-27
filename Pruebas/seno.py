# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 13:08:52 2018

@author: Lucia
"""

import matplotlib.pyplot as plt
import numpy as np

#%%
n = 100
fs = 70
Ts = 1/fs
fo = 50
fase = np.pi/2 * 0

rangon = np.linspace( 0, (n-1)*Ts, n )
rangof = np.linspace( 0, fs-fs/n, n )

x = np.sin( 2*np.pi*fo*rangon + fase)
X = np.fft.fft( x )
Xmodu = abs(X) / n
Xfase = np.arctan(X.imag/X.real)

plt.close(1)
plt.figure(1)
plt.subplot(311)
plt.plot( rangon, x)
plt.grid(True)
plt.subplot(312)
plt.plot( rangof, Xmodu )
plt.grid(True)
plt.subplot(313)
plt.plot( rangof, Xfase , '-r' )
plt.ylim( -np.pi/2, np.pi/2 )
plt.grid(True)


#%%
plt.close(2)
plt.figure(2)
plt.subplot(211)
plt.plot( rangof, X.real )
plt.grid(True)
plt.subplot(212)
plt.plot( rangof, X.imag)
plt.grid(True)

