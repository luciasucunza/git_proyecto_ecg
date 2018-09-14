# Prueba con firls

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

ws1 = 0.2           #Hz
wp1 = 5.         #Hz
wp2 = 30.0          #Hz
ws2 = 50.0          #Hz

frecs = np.array([0.0, ws1, wp1, wp2, ws2, nyq_frec ])
gainsDB = np.array([atenua, atenua, ripple, ripple, atenua, atenua])
gains = 10**(gainsDB/20)

cant_coef = 1071

fir_coeff =   sig.firls(cant_coef, frecs, gains, fs=fs)
w, hh_fir = sig.freqz(fir_coeff,1)
w = w / np.pi * nyq_frec

#%%
#------PLOTEO DE LA RESPUESTA-------
plt.figure(7)
plt.plot(w,     20 * np.log10(abs(hh_fir)),     label='FIR')
plt.plot(frecs, gainsDB, 'rx',                  label='plantilla' )

plt.title('FIR con FIRLS con ' + str(cant_coef) + ' coeficientes' )
plt.xlabel('Frequencia [Hz]')
plt.ylabel('Modulo [dB]')
plt.axis([-5, nyq_frec, -80, 20])
plt.legend()

plt.grid()
plt.show()

#%%
#------FILTRADO DE LA SEÑAL Y PLOTEO-------
ECG_f_firls = sig.lfilter(fir_coeff, 1, ecg_one_lead)

plt.figure(10)
plt.plot( ecg_one_lead,   label='ECG')
plt.plot( ECG_f_firls,      label='Fir-Firls')

plt.title('ECG filtrado')
plt.ylabel('Adimensional')
plt.xlabel('Muestras (#)')
plt.legend()       

plt.grid()
plt.show()

#%%
#------CALCULO DE LA FFT -------
resf = fs/n                                 
rangof = np.arange( 0, 360 , resf)         

FFT_ecg_one_lead = np.fft.fft( ecg_one_lead )
FFT_ECG_f_firls = np.fft.fft( ECG_f_firls )              

rangof = rangof[range(n//2)]     

FFT_ecg_one_lead = abs(FFT_ecg_one_lead[range(n//2)] ) / (n//2)    
FFT_ECG_f_firls  = abs(FFT_ECG_f_firls[range(n//2)]  ) / (n//2)  


#%%
#-------Ploteo DE LA FFT --------         
plt.figure(3)
plt.plot( rangof, FFT_ecg_one_lead,   label='ECG'       )
plt.plot( rangof, FFT_ECG_f_firls,    label='Fir-Firls' )

plt.title('FFT de ECG (zoom)')
plt.ylabel('Adimensional')
plt.xlabel('Frequencia [Hz]')
plt.axis([0, nyq_frec/2, -0.01, 0.05 ])
plt.legend()

plt.grid()
plt.show()