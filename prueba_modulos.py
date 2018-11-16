import paquete.moduloSeñales as myS

ecg_one_lead, cant_muestras, fs, nyq_frec, qrs =myS.obtenerSeñal('/home/luciasucunza/git_proyecto_ecg/Filtros/TP4_ecg.mat',0)
ecg_one_lead1, cant_muestras1, fs1, nyq_frec1, anotaciones =myS.obtenerSeñal('101',1)
