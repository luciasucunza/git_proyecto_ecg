#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 10:43:53 2018

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

#Grafico de la señal
plt.figure(1)
plt.subplot( 311 )
plt.plot( t, signal[:,0] , 'g'  )
plt.title( 'Señal' )
plt.grid( True )
plt.xlim( -0.5, 10000 )

#calculo y grafico de la transformada
resf = fields.get( 'fs' )/n                         #Resolucion
rangof = np.arange( 0, 360 , resf) 
Y = np.fft.fft( signal[:,0] )
Ymodu = abs(Y)


plt.figure(2)
plt.plot( rangof, Ymodu , 'g'  )
plt.title( 'Transformada 1' )
plt.grid( True )


#calculo y grafico de la antitransformada
signalY = np.fft.ifft( Y )
signalY = signalY.real

plt.figure(1)
plt.subplot( 312 )
plt.plot( t, signalY , 'g'  )
plt.title( 'Espectro Antitransformado 1' )
plt.grid( True )
plt.xlim( -0.5, 10000 )


#calculo y grafico de la señal de error
signalerr  =  np.zeros( n, float )
signalerr = signal[:,0] - signalY

plt.figure(1)
plt.subplot( 313 )
plt.plot( t, signalerr , 'g'  )
plt.title( 'Diferencia de señales (Error)' )
plt.grid( True )
plt.xlim( -0.5, 10000 )

#Calculo y grafico de la fft de la señal de error
Yerr = np.fft.fft( signalerr )
Yerr = abs( Yerr )

plt.figure(3)
plt.plot( rangof, Yerr , 'g'  )
plt.title( 'Transformada del Error' )
plt.grid( True )

#Calculo y grafico del histograma de la señal de error
#El parametro density es para elegir que este normalizado o no
plt.figure(4)
n, bins, patches = plt.hist(signalerr, bins = np.arange( -10e-15, 10e-15, 0.5e-15), density=True )
plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title('Histograma de la señal de error')
plt.grid(True)
plt.show()


listaMax = []
for i in np.arange( 0,40980-1, 1 ):
    if signalerr[i] > 0.5e-13:
        listaMax.append(i)
        

