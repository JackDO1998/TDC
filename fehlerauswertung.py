# -*- coding: utf-8 -*-
"""
Created on Mon May 15 17:32:03 2023

@author: janga
"""

import matplotlib.pyplot as plt
import numpy as np

from scipy.signal import find_peaks
start=9.0
stop=9.9
step=0.1
speicherort="daten/"
endung=" ns.txt"
tsoll=start
while tsoll<=stop:
    
    name=str(round(tsoll,1))
    datei = speicherort + name + endung
    x=np.loadtxt(datei, usecols=[0], dtype=float)

    n, bins, patches = plt.hist(x, bins=50);
    plt.close()
    n1=np.append(n, 0)
    binsnorm=bins/tsoll
    peaks, _ = find_peaks(n1, distance=150)
    #plt.plot(binsnorm[peaks],n1[peaks],'go')
    #plt.plot(binsnorm,n1)
    tsoll=tsoll+step
    speicherdatei = open('daten.txt','a')
    speicherdatei.write(str(round(tsoll,1)))
    speicherdatei.write("     ")
    speicherdatei.write(str(float(binsnorm[peaks])))
    speicherdatei.write('\r\n')
    speicherdatei.close()

a=np.loadtxt('daten.txt', usecols=[0], dtype=float)
b=np.loadtxt('daten.txt', usecols=[1], dtype=float)
plt.plot(a,b,'r*')





