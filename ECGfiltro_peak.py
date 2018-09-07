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
Q = .5
t = np.arange(0,n,1)
    
b,a = sig.iirpeak(wo,Q)
ecg_f_peak = sig.lfilter(b,a,ecg_one_lead)


plt.figure(1)
plt.subplot(211)
plt.plot(t, ecg_f_peak,  label='Peak')
plt.legend()
plt.grid()
plt.subplot(212)
plt.plot(t, ecg_one_lead, label='Sin Filtrar')
plt.legend()
plt.grid()
plt.show()

resf = fs/n                                 
rangof = np.arange( 0, 360 , resf)         

FFT_ecg_one_lead = np.fft.fft( ecg_one_lead )
FFT_ecg_f_peak = np.fft.fft( ecg_f_peak )  

FFT_ecg_one_lead = abs( FFT_ecg_one_lead[range(n//2)]    ) / (n//2) 
FFT_ecg_f_peak = abs( FFT_ecg_f_peak[range(n//2)]    ) / (n//2) 
rangof = rangof[range(n//2)]     

plt.figure(2)
plt.subplot(211)
plt.plot(rangof, FFT_ecg_one_lead, label='Sin Filtrar')
plt.subplot(212)
plt.plot(rangof, FFT_ecg_f_peak, label='Peak')
plt.legend()
plt.grid()
plt.show()

plt.figure(3)
w,h = sig.freqz(b,a)
plt.plot(w*nyq_frec/np.pi,h)
plt.grid()
plt.show()
