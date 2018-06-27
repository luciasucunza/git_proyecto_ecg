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
signal, fields = wfdb.io.rdsamp('117', pb_dir='mitdb',   sampto = n)
ann = wfdb.rdann('117', pb_dir='mitdb', extension = 'atr',           sampto = n)

#    CALCULO DE LA FFT 
resf = fields.get( 'fs' )/n                #Resolucion
rangof = np.arange( 0, 360 , resf)         #Rango de frecuencias

Y = np.fft.fft( signal[:,0] )              #fft

frq = frq[range(n//2)]                     #porque es simetrico
Y = Y[range(n//2)]    

#  GRAFICA DE SEÑAL, ANOTACIONES Y MODULO DEL ESPECTRO
plt.figure(1)

plt.subplot(211)
plt.plot( t, signal[:,0] )
plt.title( 'Señal' )
plt.grid( True )
plt.xlim( -1, 1600 )

plt.subplot(212)
plt.plot( rangof, abs(Y)/(n//2)   , 'g' )
plt.title( 'Espectro Normalizado' )
plt.grid(True)
plt.xlim( -0.2, 70 )

plt.show()  


#   GRAFICA DE PARTE REAL E IMAGINARIA DEL ESPECTRO
plt.figure(2)

plt.subplot(211)
plt.plot( rangof, Y.real )
plt.title( 'Parte Real' )
plt.grid(True)
plt.xlim( -1, 70 )

plt.subplot(212)
plt.plot( rangof, Y.imag )           
plt.title( 'Parte Imaginaria' )
plt.grid(True)
plt.xlim( -1, 70 )

plt.show()


#   GRAFICA DE MODULO Y FASE DEL ESPECTRO
plt.figure(3)

plt.subplot(211)
plt.plot( rangof, abs(Y), 'g' )               
plt.title( 'Modulo Sin Normalizar' )
plt.grid(True)
plt.xlim( -1, 70 )

plt.subplot(212)
plt.plot( rangof, np.arctan(Y.imag/Y.real) )
plt.title( 'Fase' )
plt.grid(True)
plt.xlim( -1, 70 )

plt.show()