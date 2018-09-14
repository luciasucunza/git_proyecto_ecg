# Prueba con FIRWIN1

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
atenua = -40.

ws1 = 0.5           #Hz
wp1 = 0.9           #Hz
wp2 = 30.0          #Hz
ws2 = 50.0          #Hz

frecs_PB = np.array([wp1, wp2]) 

f_plan = np.array([0.0, ws1, wp1, wp2, ws2, nyq_frec ])
g_plan = np.array([atenua, atenua, ripple, ripple, atenua, atenua])

cant_coef = 501

num_win =   sig.firwin(cant_coef, frecs_PB, pass_zero=False, fs=fs )
w, hh_win = sig.freqz(num_win, 1)
w = w / np.pi * nyq_frec


#%%
#------PLOTEO DE LA RESPUESTA-------
plt.figure(1)
plt.plot(w,         20 * np.log10(abs(hh_win)),     label='FIR-Win' )
plt.plot(f_plan,    g_plan, 'rx',                  label='plantilla' )

plt.title('FIR con FIRWIN1')
plt.xlabel('Frequencia [Hz]')
plt.ylabel('Modulo [dB]')
#plt.axis([0, nyq_frec, -80, 5 ])
plt.legend()

plt.grid()
plt.show()


