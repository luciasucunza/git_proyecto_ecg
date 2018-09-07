import wfdb
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig


n =10500

signals, fields = wfdb.io.rdsamp('101', pb_dir='mitdb',sampfrom = 0, sampto = n)


ecg_one_lead = signals[:,0]
fs = fields.get('fs')
wo = 0.5 / (fs/2)
nyq_frec = fs / 2
t = np.arange(0,n/fs,1/fs)

sos_butter = sig.butter( 4, wo, 'highpass', False, 'sos')

ecg_f_butter = sig.sosfilt( sos_butter, ecg_one_lead )

plt.figure(1)
plt.subplot(211)
plt.legend()
plt.grid()
plt.ylim( -0.7, 1.7)
plt.plot(t, ecg_f_butter, label='Butter' )
plt.subplot(212)
plt.plot(t, ecg_one_lead, label='Sin Filtrar')
plt.legend()
plt.grid()
plt.ylim( -0.7, 1.7)
plt.show()

resf = fs/n                                 
rangof = np.arange( 0, 360 , resf)         

FFT_ecg_one_lead = np.fft.fft( ecg_one_lead )
FFT_ecg_f_butter = np.fft.fft( ecg_f_butter )  

FFT_ecg_one_lead = abs( FFT_ecg_one_lead[range(n//2)]    ) / (n//2) 
FFT_ecg_f_butter = abs( FFT_ecg_f_butter[range(n//2)]    ) / (n//2) 
rangof = rangof[range(n//2)]     

plt.figure(2)
plt.plot(rangof, FFT_ecg_one_lead, label='Sin Filtrar')
plt.plot(rangof, FFT_ecg_f_butter, label='Butter')
plt.legend()
plt.grid()
plt.show()

plt.figure(3)
w,h = sig.sosfreqz( sos_butter )
plt.plot(w*nyq_frec/np.pi,h)
plt.grid()
plt.show()