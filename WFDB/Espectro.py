# Modulos importantantes
import wfdb
import matplotlib.pyplot as plt
import numpy as np


#%%
#------Apertura de la Señal y Anotaciones-------
n = 60000                                   #cantidad de muestras
t = np.arange( 0, n, 1 )                    #rango de muestras

signal, fields  = wfdb.io.rdsamp( '117', pb_dir='mitdb',     sampto = n                      )
ann             = wfdb.rdann(     '117', pb_dir='mitdb',     sampto = n, extension = 'atr'   )


#%%
#------Calculo de la FFT-------
resf    = fields.get( 'fs' )/n                #Resolucion
rangof  = np.arange( 0, 360 , resf)         #Rango de frecuencias

Y       = np.fft.fft( signal[:,0] )              #fft

rangof  = rangof[range(n//2)]              #Por simetría          
Y       = Y[range(n//2)]                        


#%%
#------Plote de la Señal, Anotaciones y Modulo del Espectro-------
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


#%%
#------Plote de parte Real e Imaginaria del Espectro-------
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


#%%
#------Plote de parte Real e Imaginaria del Espectro-------
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
