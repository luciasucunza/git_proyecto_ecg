import wfdb
import matplotlib.pyplot as plt
import numpy as np


n = 40980
t = np.arange( 0, n, 1 )                           

#Apertura de la señal
signal, fields = wfdb.io.rdsamp('101', pb_dir='mitdb',   sampto = n)

#Calculo de la fft
resf = fields.get( 'fs' )/n                         
rangof = np.arange( 0, 360 , resf) 
Y = np.fft.fft( signal[:,0] )
Ymodu = abs(Y)

#   Grafico de la señal y de la transformada 
plt.figure(1)
plt.subplot( 211 )
plt.plot( t, signal[:,0] , 'g'  )
plt.title( 'Señal' )
plt.grid( True )
plt.xlim( -0.5, 10000 )

plt.subplot( 212 )
plt.plot( rangof, Ymodu , 'g'  )
plt.title( 'Transformada 1' )
plt.grid( True )

#Teorema de Parseval
termino1 = 0 
for i in range (0, 40980, 1):
    termino1 = termino1 + (signal[i,0])**2

termino2 = 0
for i in range (0, 40980, 1):
    termino2 = termino2 + (Ymodu[i])**2/n

if termino1 == termino2:
    print("Teorema comprobado")
else:
    print("ERROR")
