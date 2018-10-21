#Filtro Notch elimina 60Hz

import wfdb
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig


n = 10000

signals, fields = wfdb.io.rdsamp('101', pb_dir='mitdb',sampfrom = 0, sampto = n)


ecg_one_lead = signals[:,0]
fs = fields.get('fs')
nyq_frec = fs / 2
t = np.arange(0,n/fs,1/fs)
    
Q = 100
wo = 60 / (fs/2)
b,a = sig.iirnotch(wo,Q)
ecg_f_notch = sig.lfilter(b,a,ecg_one_lead)


plt.figure(1)
plt.title('Señales')
plt.plot(t, ecg_f_notch,  label='Notch')
plt.plot(t, ecg_one_lead,  label='Sin Filtrar')
plt.grid()
plt.legend()
plt.show()


resf = fs/n                                 
rangof = np.arange( 0, 360 , resf)         

FFT_ecg_one_lead = np.fft.fft( ecg_one_lead )
FFT_ecg_f_notch = np.fft.fft( ecg_f_notch )  

FFT_ecg_one_lead = abs( FFT_ecg_one_lead[range(n//2)]    ) / (n//2) 
FFT_ecg_f_notch = abs( FFT_ecg_f_notch[range(n//2)]    ) / (n//2) 
rangof = rangof[range(n//2)]     

plt.figure(2)
plt.title('FFT de las señales')
plt.plot(rangof, FFT_ecg_one_lead, label='Sin Filtrar')
plt.plot(rangof, FFT_ecg_f_notch,  label='Notch')
plt.grid()
plt.legend()
plt.show()

w,h = sig.freqz(b,a)

plt.figure(3)
plt.title('Respuesta del Filtro')
plt.subplot(211)
plt.plot(w*nyq_frec/np.pi,abs(h))
plt.grid()
plt.ylabel('Modulo')
plt.subplot(212)
plt.plot(w*nyq_frec/np.pi, np.arctan(h.imag/h.real))
plt.grid()
plt.ylabel('Fase')
plt.show()


import scipy.signal as sig
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio


#------APERTURA DE LA SEÑAL-------
mat_struct = sio.loadmat('/home/luciasucunza/git_proyecto_ecg/Filtros/TP4_ecg.mat')

ecg_one_lead  = mat_struct['ecg_lead']
ecg_one_lead  = ecg_one_lead.flatten()
cant_muestras = len(ecg_one_lead)

fs = 1000
nyq_frec = fs / 2
