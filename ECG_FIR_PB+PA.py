# Prueba con dos filtrados

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
#------DISEÑO DE FILTROS y PLANTILLA-------
ripple = -0.05
atenua = -40.

#------Pasa Bajos-------
wpb_p           = 40.0          #Hz
wpb_s           = 50.0          #Hz
cant_coef_pb    = 201

frecs_pb    = np.array([0.0,    wpb_p,  wpb_s,  nyq_frec ])
gainsDB_pb  = np.array([ripple, ripple, atenua, atenua   ])
gains_pb = 10**(gainsDB_pb/20)

fir_coeff_pb    = sig.firls( cant_coef_pb, frecs_pb, gains_pb, fs=fs )
w_pb, hh_fir_pb = sig.freqz( fir_coeff_pb, 1 )
w_pb = w_pb / np.pi * nyq_frec

#------Pasa Altos-------
wpa_s           = 0.2          #Hz
wpa_p           = 2.0          #Hz
cant_coef_pa    = 301

frecs_pa    = np.array([0.0,    wpa_s,  wpa_p,  nyq_frec ])
gainsDB_pa  = np.array([atenua, atenua, ripple, ripple   ])
gains_pa = 10**(gainsDB_pa/20)

fir_coeff_pa    = sig.firls( cant_coef_pa, frecs_pa, gains_pa, fs=fs )
w_pa, hh_fir_pa = sig.freqz( fir_coeff_pa, 1 )
w_pa = w_pa / np.pi * nyq_frec

#------Plantilla-------
frecs   = np.array([ 0.0,    wpa_s,  wpa_p,  wpb_p,  wpb_s,  nyq_frec ])
gainsDB = np.array([ atenua, atenua, ripple, ripple, atenua, atenua   ])


#------PA * PB-------
fir_coeff = sig.convolve( fir_coeff_pa, fir_coeff_pb, method = 'direct')
_, hh_fir = sig.freqz( fir_coeff, 1 )

#%%
#------PLOTEO DE LAS RESPUESTAS-------
plt.figure(1)
plt.plot(w_pb,     20 * np.log10(abs(hh_fir_pb)),      label='FIR-PB')
plt.plot(w_pa,     20 * np.log10(abs(hh_fir_pa)),      label='FIR-PA')
plt.plot(frecs, gainsDB, 'rx',                      label='plantilla' )

plt.title('FIR con PA y PB' )
plt.xlabel('Frequencia [Hz]')
plt.ylabel('Modulo [dB]')
plt.axis([-5, nyq_frec, -50, 5])

plt.legend()
plt.grid()
plt.show()


plt.figure(2)
plt.plot( w_pa, 20 * np.log10(abs(hh_fir)),    label='FIR PB*PA')
plt.plot( frecs, gainsDB, 'rx',              label='plantilla' )

plt.title('FIR con PA*PB' )
plt.xlabel('Frequencia [Hz]')
plt.ylabel('Modulo [dB]')
plt.axis([-5, nyq_frec, -50, 5])

plt.legend()
plt.grid()
plt.show()


#%%
#------FILTRADO DE LA SEÑAL Y PLOTEO-------
ECG_f_PBPA = sig.lfilter(fir_coeff, 1, ecg_one_lead)

plt.figure(3)
plt.plot( ecg_one_lead,   label='ECG', lw=2)
plt.plot( ECG_f_PBPA,      label='Fir')

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
FFT_ECG_f_PBPA = np.fft.fft( ECG_f_PBPA )              

rangof = rangof[range(n//2)]     

FFT_ecg_one_lead = abs(FFT_ecg_one_lead[range(n//2)] ) / (n//2)    
FFT_ECG_f_PBPA    = abs(FFT_ECG_f_PBPA[range(n//2)]    ) / (n//2)  


#%%
#-------Ploteo DE LA FFT --------         
plt.figure(4)
plt.plot( rangof, FFT_ecg_one_lead,   label='ECG')
plt.plot( rangof, FFT_ECG_f_PBPA,      label='PB*PA')

plt.title('FFT de ECG (zoom)')
plt.ylabel('Adimensional')
plt.xlabel('Frequencia [Hz]')
plt.axis([0, nyq_frec/2, -0.01, 0.05 ])
plt.legend()

plt.grid()
plt.show()
#%%