import wfdb
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig


n = 50000

signals, fields = wfdb.io.rdsamp('101', pb_dir='mitdb',sampfrom = 0, sampto = n)

ecg_one_lead = signals[:,0]
fs = fields.get('fs')
nyq_frec = fs / 2

ripple = 0.5
atenuacion = 40.

ws1 = 1.0           #Hz
wp1 = 3.0           #Hz
wp2 = 15.0          #Hz
ws2 = 35.0          #Hz

frecs = np.array([0.0,         ws1,         wp1,     wp2,     ws2,         nyq_frec   ]) / nyq_frec
gains = np.array([-atenuacion, -atenuacion, -ripple, -ripple, -atenuacion, -atenuacion])
gains = 10**(gains/20)


#Devuelvue los parametros del filtro según el tipo que quiero, las frecuencias, las atenuaciones
bp_sos_butter = sig.iirdesign(wp=np.array([wp1, wp2]) / nyq_frec, ws=np.array([ws1, ws2]) / nyq_frec, gpass=ripple, gstop=atenuacion, analog=False, ftype='butter', output='sos')
bp_sos_cheby = sig.iirdesign(wp=np.array([wp1, wp2]) / nyq_frec, ws=np.array([ws1, ws2]) / nyq_frec, gpass=ripple, gstop=atenuacion, analog=False, ftype='cheby1', output='sos')
bp_sos_cauer = sig.iirdesign(wp=np.array([wp1, wp2]) / nyq_frec, ws=np.array([ws1, ws2]) / nyq_frec, gpass=ripple, gstop=atenuacion, analog=False, ftype='ellip', output='sos')

cant_coef = 501
den = 1.0
num_win =   sig.firwin2(cant_coef, frecs, gains , window='blackmanharris' )



# el _ es porque todo devuelve lo mismo,no?
# Devuelve un vector de frecuencias y un vector con sus respuestas
w, h_butter = sig.sosfreqz(bp_sos_butter)
_, h_cheby = sig.sosfreqz(bp_sos_cheby)
_, h_cauer = sig.sosfreqz(bp_sos_cauer)
_, hh_win = sig.freqz(num_win, den)

w = w / np.pi * nyq_frec

plt.plot(w, 20*np.log10(np.abs(h_butter)),  label='IIR-Butter' )
plt.plot(w, 20*np.log10(np.abs(h_cheby)),   label='IIR-Cheby' )
plt.plot(w, 20*np.log10(np.abs(h_cauer)),   label='IIR-Cauer' )
plt.plot(w, 20 * np.log10(abs(hh_win)),     label='FIR-Win')
plt.plot(frecs * nyq_frec, 20*np.log10(gains), 'rx', label='plantilla' )

plt.title('FIR diseñado por métodos directos')
plt.xlabel('Frequencia [Hz]')
plt.ylabel('Modulo [dB]')
plt.axis([0, nyq_frec, -60, 5 ]);

plt.grid()
plt.show()


#si aca utilizace el comando sosfilt me lo haría lineal?
#This function applies a linear digital filter twice
ECG_f_butt = sig.sosfiltfilt(bp_sos_butter, ecg_one_lead)
ECG_f_cheb = sig.sosfiltfilt(bp_sos_cheby, ecg_one_lead)
ECG_f_cauer = sig.sosfiltfilt(bp_sos_cauer, ecg_one_lead)

ECG_f_win = sig.filtfilt(num_win, den, ecg_one_lead)

plt.plot( ecg_one_lead,   label='ECG', lw=2)
plt.plot( ECG_f_butt,     label='Butter')
plt.plot( ECG_f_cheb,     label='Cheby')
plt.plot( ECG_f_cauer,    label='Cauer')
plt.plot( ECG_f_win,      label='Win')

ii = [0,n]
plt.title('ECG filtering example from ' + str(ii[0]) + ' to ' + str(ii[1]) )
plt.ylabel('Adimensional')
plt.xlabel('Muestras (#)')

axes_hdl = plt.gca()
axes_hdl.legend()
axes_hdl.set_yticks(())


plt.show()
            
