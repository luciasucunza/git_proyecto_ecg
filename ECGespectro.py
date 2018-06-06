#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  9 10:34:46 2018

@author: slucia
"""

import wfdb
import matplotlib.pyplot as plt
import numpy as np


n = 60000                                   #cantidad de muestras
t = np.arange( 0, n, 1 )                    #rango de muestras


#   APERTURA DE SEÑALES Y ANOTACIONES
signal, fields = wfdb.io.rdsamp('/home/slucia/Documentos/Se/117',   sampto = n)
ann = wfdb.rdann('/home/slucia/Documentos/Se/100', 'atr',           sampto = n)


#   CALCULO DE FFT
T = n/fields.get('fs')                      #tiempo tomado de la señal
frq = t/T                                   #rango de frecuencias

Y = np.fft.fft( signal[:,0] )              #fft normalizada
frq = frq[range(n//2)]                     #porque es simetrico
Y = Y[range(n//2)]    
Ynorm = abs(Y)/n                           #Modulo de la fft normalizada


#  GRAFICA DE SEÑAL, ANOTACIONES Y MODULO DEL ESPECTRO
plt.figure(1)
plt.subplot(211)
plt.plot( t, signal[:,0], 'b', label='Señal')
plt.plot( ann.sample, signal[ann.sample,0], 'ro',label='Anotaciones', )
plt.legend()
plt.title( 'Señal' )
plt.grid( True )
plt.xlim( -1, 1600 )

plt.subplot(212)
plt.plot( frq, Ynorm , 'g' )
plt.title( 'Espectro Normalizado' )
plt.grid(True)
plt.xlim( -0.2, 70 )
plt.ylim( 0, 0.05)

plt.show()  


#   GRAFICA DE PARTE REAL E IMAGINARIA DEL ESPECTRO
plt.figure(2)
plt.subplot(211)
plt.plot( frq, Y.real, 'g' )
plt.title( 'Parte Real' )
plt.grid(True)
plt.xlim( -1, 70 )
#plt.ylim( -.02, .02 )

plt.subplot(212)
plt.plot( frq, Y.imag, 'g' )           
plt.title( 'Parte Imaginaria' )
plt.grid(True)
plt.xlim( -1, 70 )
#plt.ylim( 0, 0.02 )

plt.show()


#   GRAFICA DE MODULO Y FASE DEL ESPECTRO
plt.figure(3)
plt.subplot(211)
plt.plot( frq, abs(Y), 'g' )               
plt.title( 'Modulo Sin Normalizar' )
plt.grid(True)
plt.xlim( -1, 70 )

plt.subplot(212)
plt.plot( frq, np.arctan(Y.imag/Y.real), 'g' )
plt.title( 'Fase' )
plt.grid(True)
plt.xlim( -1, 70 )

plt.show()
