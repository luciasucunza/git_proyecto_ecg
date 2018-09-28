# Módulos importantantes
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import scipy.interpolate as interpol

#%%
mat_struct = sio.loadmat('/home/luciasucunza/git_proyecto_ecg/EjemplosFiltros/TP4_ecg.mat')

ecg_one_lead = mat_struct['ecg_lead']
ecg_one_lead = ecg_one_lead.flatten(1)
qrs_detections = mat_struct['qrs_detections']
cant_muestras = len(ecg_one_lead)

fs = 1000 # Hz
nyq_frec = fs / 2
t = np.arange(cant_muestras) / fs

#%%
#------     -------
ventana_inf_ms = 300
ventana_sup_ms = 100

ventana_inf = int(ventana_inf_ms / 1000 * fs)
ventana_sup = int(ventana_sup_ms / 1000 * fs)
ventana_len = ventana_inf + ventana_sup 


np.zeros((2, 1))
mat = np.zeros(( ventana_len, len(qrs_detections)), dtype=int)

for j in range( len(qrs_detections) ):
    
    for i in range(ventana_len):    
        mat[i,j] = ecg_one_lead[ int(qrs_detections[j]) + i - ventana_inf  ]
        
#%%
#------Ploteo de Todos las ventanas-------
plt.figure(2)

plt.plot( mat )

plt.title('ECG filtrado')
plt.ylabel('Adimensional')
plt.xlabel('Tiempo (s)')
plt.legend()       

plt.grid()
plt.show()

#%%
#------Calculo de la mediana y de diferentes medias para cada ventana-------
mat_plantilla = np.zeros_like( mat )


median      = np.median(mat, axis=0)
mat_median  = median + mat_plantilla 


mean        = np.mean(mat, axis=0)
mat_mean    = mean + mat_plantilla 


mean_vent     = np.mean(mat[ 100:200 , :], axis=0)
mat_mean_vent = mean_vent + mat_plantilla 


mean_vent2     = np.mean(mat[ 0:250 , :], axis=0)
mat_mean_vent2 = mean_vent2 + mat_plantilla 

#%%
#------Resta y ploteo de cada ventana de la señal ECG con los diferentes parámetros  -------
ecg_median      = mat - mat_median
ecg_mean        = mat - mat_mean
ecg_mean_vent   = mat - mat_mean_vent
ecg_mean_vent2  = mat - mat_mean_vent2

plt.figure(3)

plt.subplot(311)
plt.plot( ecg_median )
plt.title('ECG Mediana')
plt.grid()
plt.axis([-10, 410, -12000, 32000])

plt.subplot(312)
plt.plot( ecg_mean )
plt.title('ECG Media')
plt.grid()
plt.axis([-10, 410, -12000, 32000])

plt.subplot(313)
plt.plot( ecg_mean_vent )
plt.title('ECG Media con Ventana')
plt.grid()
plt.axis([-10, 410, -12000, 32000])


plt.show()

#%%
#------ Interpolacion -------
# ¿Como elegir el 150?
ni = (qrs_detections[:,0]-150)
n_new = np.arange( cant_muestras )

y_median    = np.interp( n_new, ni, median     )
y_mean      = np.interp( n_new, ni, mean       )
y_mean_vent = np.interp( n_new, ni, mean_vent  )
y_mean_vent2= np.interp( n_new, ni, mean_vent2 )

plt.figure(4)
plt.subplot(211)
plt.plot( ni, median,     'bo', n_new, y_median,     'g',  label='Mediana'      )
plt.subplot(212)
plt.plot( ni, mean,       'bo', n_new, y_mean,       'g',  label='Media'        )   
plt.subplot(221)
plt.plot( ni, mean_vent,  'bo', n_new, y_mean_vent,  'g',  label='Media 100/200')
plt.subplot(222)
plt.plot( ni, mean_vent2, 'bo', n_new, y_mean_vent2, 'g',  label='Media 000/250')

plt.legend()
plt.show()

#%%
#------ Obtención y ploteo de ECG sin BL  -------
ecg_median     = ecg_one_lead - y_median
ecg_mean       = ecg_one_lead - y_mean
ecg_mean_vent  = ecg_one_lead - y_mean_vent
ecg_mean_vent2 = ecg_one_lead - y_mean_vent2

zoom_region = np.arange( 0, 100000, dtype='uint')
    
plt.figure(5)
plt.plot( ecg_one_lead[zoom_region],  'g' ,   label='ECG')
plt.grid()
plt.axis([-10, 100010, -12000, 32000])
plt.legend()
plt.show()

plt.figure(6)
plt.plot( ecg_median[zoom_region],    'b' ,   label='ECG Mediana')
plt.grid()
plt.axis([-10, 100010, -12000, 32000])
plt.legend()
plt.show()

plt.figure(7)
plt.plot( ecg_mean[zoom_region],      'b' ,   label='ECG Media')
plt.grid()
plt.axis([-10, 100010, -12000, 32000])
plt.legend()
plt.show()

plt.figure(8)
plt.plot( ecg_mean_vent[zoom_region], 'b' ,   label='ECG Media de 100 a 200')
plt.grid()
plt.axis([-10, 100010, -12000, 32000])
plt.legend()
plt.show()

plt.figure(9)
plt.plot( ecg_mean_vent2[zoom_region],'b' ,   label='ECG Media de 0 a 250')
plt.grid()
plt.axis([-10, 100010, -12000, 32000])
plt.legend()
plt.show()

#%%
f1= interpol.interp1d( ni, median, kind='cubic')
y1 = f1(n_new)

plt.figure(5)
plt.plot( ni, median, 'bo', n_new, y1, 'g')
plt.show()
