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


#   APERTURA DE SEÑALES Y ANOTACIONES
signal, fields = wfdb.io.rdsamp('/home/slucia/Documentos/Se/222',   sampto = n )
t = np.arange( 0, n, 1 )                            #rango de muestras

#   CALCULO DE FFT
resf = fields.get( 'fs' )/n                         #Resolucion
frq = np.arange( 0, 360 , resf)                     #Rango de frecuencias
frq = frq[range( n//2 )]                            #Mitad de Rdf por ser simetrica la fft

Y = np.fft.fft( signal[:,0] )                       #fft 
Ymedi = Y[range( n//2 )]                            #Media fft por ser simetrica
Ymodu = abs( Ymedi )                                #Modulo de la media fft
Ynorm = Ymodu / n                                   #Modulo de la media fft normalizada


#   RECORTE DEL ESPECTRO PARA CIERTO PORCENTAJE DE ENERGIA
YR = np.zeros( n//2, complex )
i = 0  
areaY = 0
porcentaje = 0.95

    #Calculo de la integral entre 0 y ts/2 de Ynorm²
for i in range( n//2 ):
    areaY = areaY + ( (Ynorm[i])**2 )*resf
    
    #Obtencion del espectro (for hasta -1 para tomar el valor de i=0)
areaVariable = areaY
for i in  np.arange( n//2-1, -1, -1 ):
    if areaVariable  > ( porcentaje*areaY ):
        areaVariable  = areaVariable  - ( (Ynorm[i])**2 )*resf
        YR[i] = 0 
        frecCorte = frq[i]
    else:
        YR[i] = Y[i]
        
        
YmoduR = abs( YR )                                          #Modulo de la media fft
YnormR = YmoduR / n                                         #Modulo de la media fft normalizada
 


#   GRAFICA DEL ESPECTRO ORIGINAL Y DEL RECORTADO
plt.figure( 1 )
plt.subplot( 211 )
plt.plot( frq, Ynorm , 'g' )
plt.title( 'Espectro Normalizado Original' )
plt.grid(True)
plt.xlim( -0.2, 70 )
plt.ylim( 0, 0.05)


plt.subplot ( 212 )
plt.plot( frq, YnormR , 'g' )
plt.title( 'Espectro Normalizado Recortado' )
plt.grid( True )
plt.xlim( -0.2, 70 )
plt.ylim( 0, 0.05 )

plt.show()  
    
    
#   CALCULO DE LA SEÑAL RECORTADA
antiYR = np.fft.ifft( YR )
antiY = np.fft.ifft( Ymedi )
tmedi = np.arange( 0, n//2, 1 )  


#   GRAFICA DE LA SEÑAL ORIGINAL Y DE LA RECORTADA
plt.figure(3)
plt.plot( tmedi, antiYR , 'g'  )
plt.title( 'Espectro Antitransformado Recortado' )
plt.grid( True )
plt.ylim( -0.65, 1.05 )
plt.xlim( -0.5, 800 )

plt.figure(4)
plt.plot( tmedi, antiY , 'g' )
plt.title( 'Espectro Antitransformado' )
plt.grid( True )
plt.ylim( -0.65, 1.05 )
plt.xlim( -0.5, 800 )    

plt.figure(5)
plt.plot( t, signal[:,0], 'g' )
plt.title( 'Espectro Original' )
plt.grid( True )
plt.ylim( -0.65, 1.05 )
plt.xlim( -0.5, 1600 )    
