
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import scipy.io as sio
import scipy.signal as sig
import scipy.interpolate as interpol
import time

import paquete.moduloSeñales as myS
import paquete.moduloFiltrado as myF

import matplotlib as mpl
import matplotlib.pyplot as plt
from pandas import DataFrame
from IPython.display import HTML
mpl.rcParams['figure.figsize'] = (15,12)  

#------APERTURA DE LA SEÑAL-------
ecg_one_lead, cant_muestras, fs, nyq_frec, qrs_detections = myS.obtenerSeñal('/home/luciasucunza/git_proyecto_ecg/Filtros/TP4_ecg.mat')
t = np.arange(cant_muestras) / fs