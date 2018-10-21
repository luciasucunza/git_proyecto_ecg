# MÃ³dulos importantantes
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import scipy.interpolate as interpol

#%%
mat_struct = sio.loadmat('/home/luciasucunza/git_proyecto_ecg/Filtros/TP4_ecg.mat')

ecg_one_lead = mat_struct['ecg_lead']
ecg_one_lead = ecg_one_lead.flatten()
qrs_detections = mat_struct['qrs_detections']
cant_muestras = len(ecg_one_lead)

fs = 1000 
nyq_frec = fs / 2
t = np.arange(cant_muestras) / fs

#%%
#------     -------
ventana_inf_ms    = 300
ventana_sup_ms    = 100

ventana_inf = int(ventana_inf_ms / 1000 * fs)
ventana_sup = int(ventana_sup_ms / 1000 * fs)
ventana_len = ventana_inf + ventana_sup 

mat = np.zeros(( ventana_len, len(qrs_detections)), dtype=int)

for j in range( len(qrs_detections) ):
    
    for i in range(ventana_len):    
        mat[i,j] = ecg_one_lead[ int(qrs_detections[j]) + i - ventana_inf  ]
        
#%%
#------Ploteo de Todos las ventanas-------
plt.figure('Todas las ventanas')

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


mean_vent2     = np.mean(mat[ 50:250 , :], axis=0)
mat_mean_vent2 = mean_vent2 + mat_plantilla 


#%%
#------Resta de cada ventana de la seÃ±al ECG con los diferentes parÃ¡metros  -------
ecg_median      = mat - mat_median
ecg_mean        = mat - mat_mean
ecg_mean_vent   = mat - mat_mean_vent
ecg_mean_vent2  = mat - mat_mean_vent2


#%%
#------Ploteo de cada ventana de la seÃ±al ECG con los diferentes parÃ¡metros  -------

plt.figure('Ventanas con su correspondiente parametro restado')

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
n_new       = np.arange( cant_muestras )

ni                      = np.zeros( len(qrs_detections)+2)
ni[0]                   = 0
ni[1:1904]              = ( qrs_detections[:,0] - int((ventana_inf_ms)/2) )
ni[1904]                = cant_muestras

median_aux              = np.zeros( len(qrs_detections)+2)
median_aux[0]           = median[0] 
median_aux[1:1904]      = median
median_aux[1904]        = median[1902]

mean_aux                = np.zeros( len(qrs_detections)+2)
mean_aux[0]             = mean[0] 
mean_aux[1:1904]        = mean
mean_aux[1904]          = mean[1902]

mean_vent_aux           = np.zeros( len(qrs_detections)+2)
mean_vent_aux[0]        = mean_vent[0] 
mean_vent_aux[1:1904]   = mean_vent
mean_vent_aux[1904]     = mean_vent[1902]

mean_vent2_aux          = np.zeros( len(qrs_detections)+2)
mean_vent2_aux[0]       = mean_vent2[0] 
mean_vent2_aux[1:1904]  = mean_vent2
mean_vent2_aux[1904]    = mean_vent2[1902]


f= interpol.interp1d( ni, median_aux,       kind='cubic')
y_median        = f(n_new)

f= interpol.interp1d( ni, mean_aux,         kind='cubic')
y_mean          = f(n_new)

f= interpol.interp1d( ni, mean_vent_aux,    kind='cubic')
y_mean_vent     = f(n_new)

f= interpol.interp1d( ni, mean_vent2_aux,   kind='cubic')
y_mean_vent2    = f(n_new)
#%%
#------ Ploteo Interpolacion -------
plt.figure('Interpolacion de los parametros de cada ventana')
plt.subplot(221)
plt.title('Mediana')
plt.plot( ni, median_aux,     'bo', n_new, y_median,     'g' )
plt.subplot(222)
plt.title('Media')
plt.plot( ni, mean_aux,       'bo', n_new, y_mean,       'g' )
plt.subplot(223)
plt.title('Mediana con ventana 100/200')
plt.plot( ni, mean_vent_aux,  'bo', n_new, y_mean_vent,  'g' )
plt.subplot(224)
plt.title('Mediana con ventana 050/250')
plt.plot( ni, mean_vent2_aux, 'bo', n_new, y_mean_vent2, 'g' )
plt.show()

#%%
#------ ObtenciÃon de ECG sin BL  -------
ecg_median     = ecg_one_lead - y_median
ecg_mean       = ecg_one_lead - y_mean
ecg_mean_vent  = ecg_one_lead - y_mean_vent
ecg_mean_vent2 = ecg_one_lead - y_mean_vent2

zoom_region = np.arange( 0, 100000, dtype='uint')
#%%
#------ Ploteo de ECG sin BL  -------
plt.figure('Señales Obtenidas')

plt.plot( ecg_one_lead[zoom_region],    label='ECG'                     )
plt.plot( ecg_median[zoom_region],      label='ECG Mediana'             )
plt.plot( ecg_mean[zoom_region],        label='ECG Media'               )
plt.plot( ecg_mean_vent[zoom_region],   label='ECG Media de 100 a 200'  )
plt.plot( ecg_mean_vent2[zoom_region],  label='ECG Media de 050 a 250'  )

plt.grid()
plt.axis([-10, 100010, -12000, 32000])
plt.legend()
plt.show()
