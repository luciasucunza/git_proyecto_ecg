# MÃ³dulos importantantes
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import scipy.signal as sig

#%%
mat_struct = sio.loadmat('/home/luciasucunza/git_proyecto_ecg/EjemplosFiltros/TP4_ecg.mat')

ecg_one_lead = mat_struct['ecg_lead']
ecg_one_lead = ecg_one_lead.flatten(1)
cant_muestras = len(ecg_one_lead)

fs = 1000 
nyq_frec = fs / 2
t = np.arange(cant_muestras) / fs

c_muestras_zoom = 60000

zoom_region     = np.arange(0, c_muestras_zoom , 1)
ecg_zoom        = ecg_one_lead[zoom_region]
t_zoom          = t[zoom_region]

#%%
baseline = sig.medfilt (ecg_zoom, kernel_size = int (np.around(fs*0.5*0.2)    *2 +1  ))
baseline = sig.medfilt (baseline, kernel_size = int (np.around(fs*0.5*0.6)    *2 +1  )) 
baseline = sig.medfilt (baseline, kernel_size = int (np.around(fs*0.5*(1/50)) *2 +1  ))

plt.figure(1)
plt.title('Señales')
plt.plot(t_zoom, ecg_zoom,  label='ECG')
plt.plot(t_zoom, baseline,  label='Baseline')
plt.grid()
plt.legend()
plt.show()

#%%
ecg_F = ecg_zoom - baseline

plt.figure(2)
plt.title('Señales')
plt.plot(t_zoom, ecg_zoom,  label='ECG sin flitrar')
plt.plot(t_zoom, ecg_F,     label='ECG flitrarado')
plt.grid()
plt.legend()
plt.show()

#%%


#Calculo auxiliar para ver la componente, 50Hz
resf = fs/c_muestras_zoom                           #Resolucion
rangof = np.arange( 0, fs , resf)         #Rango de frecuencias
F_ecg_zoom = np.fft.fft( ecg_zoom )              #fft
F_ecg_zoom =  abs(F_ecg_zoom)/(c_muestras_zoom) 
plt.figure(1)
plt.plot( rangof, F_ecg_zoom  , 'g' )
plt.title( 'Espectro Normalizado' )
plt.grid(True)
plt.xlim( -0.2, 70 )
plt.show() 