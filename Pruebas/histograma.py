#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 12:56:27 2018

@author: slucia
"""
import wfdb
import matplotlib.pyplot as plt
import numpy as np


n = 40980
t = np.arange( 0, n, 1 )                           

#apertura
signal, fields = wfdb.io.rdsamp('/home/slucia/Documentos/Se/101',   sampto = n)
ann = wfdb.rdann('/home/slucia/Documentos/Se/100', 'atr',           sampto = n)

#antitransformo/transformo
resf = fields.get('fs') / n
rangof = np.arange( 0, fields.get('fs'), resf )
Y = np.fft.fft( signal[:,0] )
signalY = np.fft.ifft( Y )
signalY = signalY.real

signalerr  =  np.zeros( n, float )
signalerr = signal[:,0] - signalY

#array([  156,   322,   875, 20988, 14687,  3040,   639,   167,   106])

histograma = np.zeros( 9, int )

for i in  np.arange( n-1, -1, -1 ):
        
    if signalerr[i] < -4e-15:
        histograma[0] = histograma[0] + 1 
    else:
        if signalerr[i] < -3e-15:
            histograma[1] = histograma[1] + 1 
        else:
            if signalerr[i] < -2e-15:
                histograma[2] = histograma[2] + 1 
            else:                            
                if signalerr[i] < 0:
                    histograma[3] = histograma[3] + 1 
                else:       
                    if signalerr[i] < 1e-15:
                        histograma[4] = histograma[4] + 1 
                    else:
                        if signalerr[i] < 2e-15:
                            histograma[5] = histograma[5] + 1 
                        else:
                            if signalerr[i] < 3e-15:
                                histograma[6] = histograma[6] + 1 
                            else:
                                if signalerr[i] < 4e-15:
                                    histograma[7] = histograma[7] + 1 
                                else:
                                    if signalerr[i] > 4e-15:
                                        histograma[8] = histograma[8] + 1 
                                        
plt.plot(np.arange( 0, 9, 1 ), histograma)
plt.title( 'Histograma' )
plt.grid( True )