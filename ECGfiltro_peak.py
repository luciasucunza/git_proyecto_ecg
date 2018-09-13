# Filtro pasa altos 0.5Hz

import wfdb
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig


n = 10500

signals, fields = wfdb.io.rdsamp('101', pb_dir='mitdb',sampfrom = 0, sampto = n)


ecg_one_lead = signals[:,0]
fs = fields.get('fs')
wo = 4 / (fs/2)
nyq_frec = fs / 2
Q = 1
t = np.arange(0,n,1)
    
b,a = sig.iirpeak(wo,Q)
ecg_f_peak = sig.lfilter(b,a,ecg_one_lead)


plt.figure(1)
plt.subplot(211)
plt.title('Señales')
plt.plot( t, ecg_f_peak )
plt.ylabel('Peak')
plt.grid()
plt.subplot(212)
plt.plot( t, ecg_one_lead )
plt.ylabel('Sin Filtrar')
plt.grid()
plt.show()

resf = fs/n                                 
rangof = np.arange( 0, 360 , resf)         

FFT_ecg_one_lead = np.fft.fft( ecg_one_lead )
FFT_ecg_f_peak = np.fft.fft( ecg_f_peak )  

FFT_m_ecg_one_lead = abs( FFT_ecg_one_lead[range(n//2)]    ) / (n//2) 
FFT_m_ecg_f_peak = abs( FFT_ecg_f_peak[range(n//2)]    ) / (n//2) 
rango = rangof[range(n//2)]     

plt.figure(2)
plt.subplot(211)
plt.title('FFT de las señales')
plt.plot(rango, FFT_m_ecg_one_lead)
plt.ylim( -0.005, 0.05)
plt.ylabel('SinFiltrar')
plt.grid()
plt.subplot(212)
plt.plot(rango, FFT_m_ecg_f_peak)
plt.grid()
plt.ylim( -0.005, 0.05)
plt.ylabel('Peak')
plt.show()


FFT_f_ecg_one_lead = np.arctan( FFT_ecg_f_peak.imag/FFT_ecg_f_peak.real )
FFT_f_ecg_f_peak = np.arctan( FFT_ecg_f_peak.imag/FFT_ecg_f_peak.real ) 

w,h = sig.freqz(b,a)
plt.figure(4)
plt.subplot(211)
plt.title('Respuesta del Filtro')
plt.plot(w*nyq_frec/np.pi,abs(h))
plt.grid()
plt.ylabel('Modulo')
plt.subplot(212)
plt.plot(w*nyq_frec/np.pi, np.arctan(h.imag/h.real)  )
plt.grid()
plt.ylabel('Fase')
plt.show()
