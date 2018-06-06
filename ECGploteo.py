#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  9 13:25:05 2018

@author: slucia
"""

import wfdb
import matplotlib.pyplot as plt
import numpy as np


#   APERTURA DE SEÑALES Y ANOTACIONES
signals1, fields1 = wfdb.io.rdsamp('101', pb_dir='mitdb',           sampfrom = 0, sampto = 20)
annS1 = wfdb.rdann('/home/slucia/Documentos/Se/101', 'atr',         sampfrom = 0, sampto = 20)

signals2, fields2 = wfdb.io.rdsamp('/home/slucia/Documentos/Se/201',sampfrom = 0, sampto = 50)
annS2 = wfdb.rdann('/home/slucia/Documentos/Se/201', 'atr',         sampfrom = 0, sampto = 50)

record1 = wfdb.io.rdrecord('/home/slucia/Documentos/Se/101',        sampfrom = 0, sampto = 30)
annR1 = wfdb.rdann('/home/slucia/Documentos/Se/101', 'atr',         sampfrom = 0, sampto = 30)

record2 = wfdb.io.rdrecord('/home/slucia/Documentos/Se/201',        sampfrom = 0, sampto = 70)
annR2 = wfdb.rdann('/home/slucia/Documentos/Se/201', 'atr',         sampfrom = 0, sampto = 70)



#   PLOTEO CON FUNCIONES PROPIAS
plt.figure(2)

plt.subplot(211)
t1 = np.arange( 0, 20, 1 )
plt.plot( t1, signals1[:,0],  label='Señal')
plt.plot(annS1.sample, signals1[annS1.sample,0], 'ro',label='Anotaciones', )
plt.ylabel('Señal101')
plt.grid(True)
plt.legend()

plt.subplot(212)
t2 = np.arange( 0, 50, 1 )
plt.plot( t2, signals2[:,0],  label='Señal')
plt.plot(annS2.sample, signals2[annS2.sample,0], 'ro',label='Anotaciones', )
plt.ylabel('Señal 201')
plt.grid(True)
plt.legend()


plt.xlabel('$Muestras$')
plt.show()



plt.figure(3)

plt.subplot(211)
t1 = np.arange( 0, 30, 1 )
plt.plot( t1, record1.p_signal[:,0],  label='Señal')
plt.plot(annR1.sample, record1.p_signal[annR1.sample,0], 'ro',label='Anotaciones', )
plt.ylabel('Señal101')
plt.grid(True)
plt.legend()

plt.subplot(212)
t2 = np.arange( 0, 70, 1 )
plt.plot( t2, record2.p_signal[:,0],  label='Señal')
plt.plot(annR2.sample, record2.p_signal[annR2.sample,0], 'ro',label='Anotaciones', )
plt.ylabel('Señal 201')
plt.grid(True)
plt.legend()


plt.xlabel('$Muestras$')
plt.show()


plt.figure(4)

plt.subplot(211)
t1 = np.arange( 0, 20, 1 )
plt.plot( t1, signals1[:,1],  label='Señal')
plt.plot(annS1.sample, signals1[annS1.sample,1], 'ro',label='Anotaciones', )
plt.ylabel('Señal101b')
plt.grid(True)
plt.legend()

plt.subplot(212)
t2 = np.arange( 0, 50, 1 )
plt.plot( t2, signals2[:,1],  label='Señal')
plt.plot(annS2.sample, signals2[annS2.sample,1], 'ro',label='Anotaciones', )
plt.ylabel('Señal 201b')
plt.grid(True)
plt.legend()


plt.xlabel('$Muestras$')
plt.show()

