# Prueba con remaz
#COMO HACER PARA GRAFICAR LA PLANTILLA, PARA HACER QUE EL VECTOR SEA COMO CONTRARIO RANGE(//2) 

import wfdb
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig

#%%
#------APERTURA DE LA SEÑAL-------
n = 10500

signals, fields = wfdb.io.rdsamp('101', pb_dir='mitdb',sampfrom = 0, sampto = n)

ecg_one_lead = signals[:,0]
fs = fields.get('fs')
nyq_frec = fs / 2


#%%
#------DISEÑO DE FILTRO-------
ripple = -0.5
atenua = -70.

ws1 = 1.0           #Hz
wp1 = 4.0           #3Hz
wp2 = 15.0          #Hz
ws2 = 35.0          #Hz

frecs = np.array([0.0, ws1, wp1, wp2, ws2, nyq_frec ])
gains = np.array([atenua, ripple, atenua])
gains = 10**(gains/20)

cant_coef = 72

fir_coeff = sig.remez(cant_coef, frecs, gains, fs=fs)
w, hh_fir = sig.freqz(fir_coeff)
w = w / np.pi * nyq_frec

#%%
#------PLOTEO DE LA RESPUESTA-------
plt.figure(1)
plt.plot(w,     20 * np.log10(abs(hh_fir)),     label='FIR')
#plt.plot(frecs, 20*np.log10(gains), 'rx',       label='plantilla' )

plt.title('FIR con FIRLS')
plt.xlabel('Frequencia [Hz]')
plt.ylabel('Modulo [dB]')
#plt.axis([0, nyq_frec, -80, 5 ])
plt.legend()

plt.grid()
plt.show()

#%%
#------FILTRADO DE LA SEÑAL Y PLOTEO-------



#%%
#------CALCULO DE LA FFT -------


#%%
#-------Ploteo DE LA FFT --------         
