#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 16 11:48:38 2018

@author: slucia
"""


import wfdb
import matplotlib.pyplot as plt
import numpy as np

n = 40980                                           #cantidad de muestras
t = np.arange( 0, n, 1 )                            #rango de muestras


#   APERTURA DE SEÑAL y CALCULO DE LA FFT
#%%
signal, fields = wfdb.io.rdsamp('101', pb_dir='mitdb',   sampto = n)

resf = fields.get( 'fs' )/n                         #Resolucion
rangof = np.arange( 0, 360 , resf)                  #Rango de frecuencias

Y = np.fft.fft( signal[:,0] )                       #fft 
Ymodu = abs( Y )                                    #Modulo de la media fft


#   CALCULO DE LA FFT RECORTADA PARA CIERTO PORCENTAJE DE ENERGIA
#%% 
Ymitad = Ymodu[range(n//2)] 
YR = np.zeros( n, complex )
i = 0  
areaY = 0
porcentaje = 0.98

    #Calculo de la integral entre 0 y ts/2 de Ynorm²
for i in range( n//2 ):
    areaY = areaY + ( (Ymitad[i])**2 )*resf
    
    #Obtencion del espectro (for hasta -1 para tomar el valor de i=0)
areaVariable = areaY
for i in  np.arange( n//2-1, -1, -1 ):
    if areaVariable  > ( porcentaje*areaY ):
        areaVariable  = areaVariable  - ( (Ymitad[i])**2 )*resf
        YR[i] = 0 

        frecCorte = rangof[i]
    else:
        YR[i] = Y[i]
        YR[n-1-i] = Y[n-1-i]
        
    # Aca si copio Y{n} se me modifica porque el ultimo valor no es simetrtico!!              
YmoduR = abs( YR )


#   CALCULO DE ANTITRANSFORMADA DE LA FFT RECORTADA
#%%
signalYR = np.fft.ifft( YR )
signalYR = signalYR.real



#   GRAFICA DEL ESPECTRO ORIGINAL Y DEL RECORTADO
#%% 
plt.figure( 1 )
plt.subplot( 211 )
plt.plot( rangof, Ymodu , 'g' )
plt.title( 'Espectro Original' )
plt.grid(True)

plt.subplot ( 212 )
plt.plot( rangof, YmoduR , 'b' )
plt.title( 'Espectro Recortado' )
plt.grid( True )

plt.show()  

    
#   GRAFICO DE LA SEÑAL Y DE LA SEÑAL FILTRADA
#%% 
plt.figure(3)
plt.subplot( 211 )
plt.plot( t, signal[:,0], 'g'  )
plt.title( 'Señal Original' )
plt.grid( True )
plt.ylim( -0.65, 1.05 )
plt.xlim( -0.5, 1600 )

plt.subplot( 212 )
plt.plot( t, signalYR , 'b' )
plt.title( 'Señal Filtrada' )
plt.grid( True )
plt.ylim( -0.65, 1.05 )
plt.xlim( -0.5, 1600 ) 
