import wfdb
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig


n = 10000

signals, fields = wfdb.io.rdsamp('101', pb_dir='mitdb',sampfrom = 0, sampto = n)


ecg_one_lead = signals[:,0]
fs = fields.get('fs')
wo = 60 / (fs/2)
nyq_frec = fs / 2
Q = 100


b,a = sig.iirnotch(wo,Q)
ecg_f_notch = sig.lfilter(b,a,ecg_one_lead)

t = np.arange(0,n,1)

plt.figure(1)
plt.plot(t, ecg_f_notch)
plt.plot(t, ecg_one_lead)
plt.show()


resf = fs/n                                 
rangof = np.arange( 0, 360 , resf)         

FFT_ecg_one_lead = np.fft.fft( ecg_one_lead )
FFT_ecg_f_notch = np.fft.fft( ecg_f_notch )  

FFT_ecg_one_lead = abs( FFT_ecg_one_lead[range(n//2)]    ) / (n//2) 
FFT_ecg_f_notch = abs( FFT_ecg_f_notch[range(n//2)]    ) / (n//2) 
rangof = rangof[range(n//2)]     

plt.figure(2)
plt.plot(rangof, FFT_ecg_one_lead)
plt.plot(rangof, FFT_ecg_f_notch)
plt.show()


w,h = sig.freqz(b,a)
plt.plot(w*nyq_frec/np.pi,h)
