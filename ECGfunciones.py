#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 15:11:23 2018

@author: luciasucunza
"""

#Uso de las herramientas de procesamiento

#Para poder detectar los complejos QRS es necesario tener al menos 109 muestras



import wfdb
from wfdb import processing

sig, fields = wfdb.rdsamp('101', pb_dir='mitdb',  channels=[0],sampfrom = 0, sampto = 109)
xqrs = processing.XQRS(sig=sig[:,0], fs=fields['fs'])
xqrs.detect()

wfdb.plot_items(signal=sig, ann_samp=[xqrs.qrs_inds])