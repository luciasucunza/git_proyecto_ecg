def medianaMovil( signali, fs ):
    
    import scipy.signal as sig 
    import numpy as np
       
    baseline = sig.medfilt (signali, kernel_size = int (np.around(fs*0.5*0.2)    *2 +1  ))
    baseline = sig.medfilt (baseline, kernel_size = int (np.around(fs*0.5*0.6)    *2 +1  )) 
    baseline = sig.medfilt (baseline, kernel_size = int (np.around(fs*0.5*(1/50)) *2 +1  ))
    
    signalo = signali - baseline
    
    return signalo, baseline



def diseñoPB( fs, wpb_p, wpb_s, cant_coef_pb ):
    
    import scipy.signal as sig 
    import numpy as np
       
    nyq_frec    = fs / 2
    ripple      = -0.05
    atenua      = -40.
    
    frecs_pb        = np.array([0.0,    wpb_p,  wpb_s,  nyq_frec ])
    gainsDB_pb      = np.array([ripple, ripple, atenua, atenua   ])
    gains_pb        = 10**(gainsDB_pb/20)
    
    fir_coeff_pb    = sig.firls( cant_coef_pb, frecs_pb, gains_pb, fs=fs )
    
    return fir_coeff_pb
    
     
    
    
def diseñoPA( fs, wpa_p, wpa_s, cant_coef_pa, modo = 1):
    
    import scipy.signal as sig 
    import numpy as np
          
    nyq_frec    = fs / 2
    ripple      = -0.05
    atenua      = -40.
    
    frecs_pa        = np.array([0.0,    wpa_s,  wpa_p,  nyq_frec ])
    gainsDB_pa      = np.array([atenua, atenua, ripple, ripple   ])
    gains_pa        = 10**(gainsDB_pa/20)

    fir_coeff_pa    = sig.firls( cant_coef_pa, frecs_pa, gains_pa, fs=fs )
 
    return fir_coeff_pa   


def convPAPB( signal_i, fs, wpb_p, wpb_s, cant_coef_pb, wpa_p, wpa_s, cant_coef_pa):

    import scipy.signal as sig 
    import numpy as np
       
    cant_muestras = len(signal_i)
    
    fir_coeff_pb = diseñoPB( fs, wpb_p, wpb_s, cant_coef_pb)
    fir_coeff_pa = diseñoPA( fs, wpa_p, wpa_s, cant_coef_pa)
    fir_coeff = sig.convolve( fir_coeff_pa, fir_coeff_pb, method = 'direct')
    
    signal_f    = sig.lfilter(fir_coeff, 1, signal_i)
    signal_o    = np.zeros(cant_muestras)

    c = int((cant_coef_pa+cant_coef_pb)/2)
    
    for i in range (0, cant_muestras-c-1):
        signal_o[i] = signal_f[ i + c]
    
    for i in range (cant_muestras-c, cant_muestras-1):
        signal_o[i] = 0  
        
    return signal_o

#def multirate( signali, qrsfs_old, fs_new):

    
#Estimador = 0 -> Media
#Estimador = 1 -> Mediana
    

def estSusraccion( signal_i, qrs_detections, fs, estimador, subV_inf = 0, subV_sup = 400 ):
  
    import numpy as np
    import scipy.interpolate as interpol
    
    ventana_inf_ms  =  300
    ventana_sup_ms  =  100
    ventana_inf     = int(ventana_inf_ms / 1000 * fs)
    ventana_sup     = int(ventana_sup_ms / 1000 * fs)
    ventana_len     = ventana_inf + ventana_sup 
    
    mat = np.zeros(( ventana_len, len(qrs_detections)), dtype=int)
    for j in range( len(qrs_detections) ):
        for i in range(ventana_len):    
            mat[i,j] = signal_i[ int(qrs_detections[j]) + i - ventana_inf  ]

    #------Calculo del estimador para cada ventana-------
    if estimador:
        est = np.median(mat[subV_inf:subV_sup , :], axis = 0)
    else:
        est = np.mean(mat[subV_inf:subV_sup , :], axis = 0)
    #------ Interpolacion -------
    n_new   = np.arange( len(signal_i) )
    
    ni                              = np.zeros( len(qrs_detections)+2)
    ni[0]                           = 0
    ni[1:len(qrs_detections)+1]     = ( qrs_detections[:,0] - int((ventana_inf_ms)/2) )
    ni[len(qrs_detections)+1]       = len(signal_i)

    est_aux                          = np.zeros( len(qrs_detections)+2 )
    est_aux[0]                       = est[0]
    est_aux[1:len(qrs_detections)+1]  = est
    est_aux[len(qrs_detections)+1]   = est[len(qrs_detections)-1]
    
    f       = interpol.interp1d( ni, est_aux, kind='cubic')
    y_est   = f(n_new)
    
    singal_o = signal_i - y_est
    
    return singal_o