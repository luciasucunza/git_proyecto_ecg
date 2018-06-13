# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 23:08:52 2018

@author: Lucia
"""

import matplotlib.pyplot as plt
import numpy as np

fs = 150
Ts = 1/fs
t = np.arange( 0, 1, Ts )
ff = 5
x=np.sin(2*np.pi*ff*t)
                    
rangof = np.arange( 0, fs, 1) 
X = np.fft.fft( x )
Xmodu = abs(X)

plt.subplot(211)
plt.plot(t,x)
plt.grid(True)
plt.subplot(212)
plt.plot(rangof, Xmodu )
plt.grid(True)