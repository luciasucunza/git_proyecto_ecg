# Modulos importantantes
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import scipy.signal as sig

#%%
#------Apertura de la Señal-------
mat_struct = sio.loadmat('/home/luciasucunza/git_proyecto_ecg/Filtros/TP4_ecg.mat')

ecg_one_lead = mat_struct['ecg_lead']
ecg_one_lead = ecg_one_lead.flatten(1)
cant_muestras = len(ecg_one_lead)

fs = 1000 
nyq_frec = fs / 2
t = np.arange(cant_muestras) / fs

#------Region de Trabajo-------
c_muestras_zoom = 112911

zoom_region     = np.arange(0, c_muestras_zoom , 1)
ecg_zoom        = ecg_one_lead[zoom_region]
t_zoom          = t[zoom_region]

#%%
#------Estimacion de la Linea de Base-------
baseline = sig.medfilt (ecg_zoom, kernel_size = int (np.around(fs*0.5*0.2)    *2 +1  ))
baseline = sig.medfilt (baseline, kernel_size = int (np.around(fs*0.5*0.6)    *2 +1  )) 
baseline = sig.medfilt (baseline, kernel_size = int (np.around(fs*0.5*(1/50)) *2 +1  ))


#%%
#------Ploteo de la Linea de Base-------
plt.figure('LineaDeBasePorMedianaZoom')
plt.title('Señales')
plt.plot(t_zoom, baseline,  label='Baseline')
plt.grid()
plt.legend()
plt.show()

#%%
#------Sustracción de Linea de Base-------
ecg_F = ecg_zoom - baseline


#%%
#------Ploteo de la Señal sin Linea de Base-------
plt.figure('FiltradoMedianaMovil')
plt.title('Señales')
plt.plot(t_zoom, ecg_zoom,  label='ECG sin flitrar')
plt.plot(t_zoom, baseline,  label='Baseline')
plt.plot(t_zoom, ecg_F,     label='ECG flitrarado')
plt.grid()
plt.legend()
plt.show()