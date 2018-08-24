#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 14:57:54 2018

@author: mllamedo

Script para ejemplificar el diseño, análisis y uso de filtros IIR

"""

import numpy as np
import scipy.signal as sig
import matplotlib as mpl
import sys

sys.path.append('/home/mariano/scripts/analog filters/python') 

from splane import analyze_sys

#####################
## Start of script ##
#####################

# Setup inline graphics
mpl.rcParams['figure.figsize'] = (10,10)
        

#%% 

############################################
## Diseño a partir de un filtro analógico ##
############################################

# Tipo de aproximación.
        
aprox_name = 'Butterworth'
#aprox_name = 'Chebyshev1'
#aprox_name = 'Chebyshev2'
#aprox_name = 'Bessel'
#aprox_name = 'Cauer'

# Requerimientos de plantilla


fc = 10e3/2/np.pi # Hz
ripple = 0.5
attenuation = 40
order2analyze = 3

# frecuencia de muestreo
fs = 5*fc

# Prewarp
fpw = fs; # sin prewarp
#fpw = np.pi*fc/np.tan(np.pi*fc/fs); # prewarp para fc



all_sys = []
analog_filters = []
digital_filters = []

filter_names = []
analog_filters_names = []
digital_filters_names = []

if aprox_name == 'Butterworth':

    z,p,k = sig.buttap(order2analyze)

elif aprox_name == 'Chebyshev1':

    z,p,k = sig.cheb1ap(order2analyze, ripple)
    
elif aprox_name == 'Chebyshev2':

    z,p,k = sig.cheb2ap(order2analyze, ripple)
    
elif aprox_name == 'Bessel':
    
    z,p,k = sig.besselap(order2analyze, norm='mag')
    
elif aprox_name == 'Cauer':
   
    z,p,k = sig.ellipap(order2analyze, ripple, attenuation)

num, den = sig.zpk2tf(z,p,k)

# Desnormalizamos para wc
num, den = sig.lp2lp(num, den, 2*np.pi*fc)

my_analog_filter = sig.TransferFunction(num,den)
my_analog_filter_desc = aprox_name + '_ord_' + str(order2analyze) + '_analog'

all_sys.append(my_analog_filter)
filter_names.append(my_analog_filter_desc)

analog_filters.append(my_analog_filter)
analog_filters_names.append(my_analog_filter_desc)

# Transformamos el filtro analógico mediante la transformada bilineal

numz, denz = sig.bilinear(num, den, fpw)

my_digital_filter = sig.TransferFunction(numz, denz, dt=1/fs)
my_digital_filter_desc = aprox_name + '_ord_' + str(order2analyze) + '_digital'

all_sys.append(my_digital_filter)
filter_names.append(my_digital_filter_desc)

# Analizamos y comparamos los filtros
analyze_sys( all_sys, filter_names )




