# -*- coding: utf-8 -*-
"""
Created on Mon May 15 17:32:03 2023

@author: janga
"""

import matplotlib.pyplot as plt
import numpy as np

from scipy.signal import find_peaks
start=12.0
stop=37.0
step=0.01
speicherort="daten/"
endung=" ns.txt"
tsoll=start
i=0
while tsoll<=stop:
    
    name=str(round(tsoll,2))
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
    speicherdatei.write(str(round(tsoll,2)))
    speicherdatei.write("     ")
    speicherdatei.write(str(float(binsnorm[peaks])))
    speicherdatei.write('\r\n')
    speicherdatei.close()
    print(i)
    i=i+1

