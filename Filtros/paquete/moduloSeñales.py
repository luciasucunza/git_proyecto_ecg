def obtenerSeñal( nombre, modo = 0):
    if modo:
        import wfdb 
        signals, fields = wfdb.io.rdsamp( '101', pb_dir = 'mitdb')
        ecg_one_lead    = signals[:,0]
        fs              = fields.get('fs')
        anotaciones     = wfdb.rdann('101', pb_dir='mitdb',extension='atr')
        anotaciones     = anotaciones.sample
    else:
        import scipy.io as sio
        mat_struct      = sio.loadmat( nombre )
        ecg_one_lead    = mat_struct['ecg_lead']
        ecg_one_lead    = ecg_one_lead.flatten(1)
        anotaciones     = mat_struct['qrs_detections']
        fs              = 1000
        
    cant_muestras   = len(ecg_one_lead)
    nyq_frec        = fs/2          

    return ecg_one_lead, cant_muestras, fs, nyq_frec, anotaciones
        