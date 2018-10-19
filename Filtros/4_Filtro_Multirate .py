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

#%%


#%%

#%%