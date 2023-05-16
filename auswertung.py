# -*- coding: utf-8 -*-
"""
Created on Mon May 15 23:15:53 2023

@author: janga
"""
import matplotlib.pyplot as plt
import numpy as np
a=np.loadtxt('daten.txt', usecols=[0], dtype=float)
b=np.loadtxt('daten.txt', usecols=[1], dtype=float)
plt.plot(a,b,'r*')
plt.grid(True)
plt.xlabel("Eingestellte Zeit in ns")
plt.ylabel('relative Abweichung')
plt.title('Gesamtplot')
plt.savefig('Gesamtplot.pdf')
plt.close()
j=0
h=1
while h<=25:
    a1=[]
    b1=[]
    while j<=(h*100)-1:
        a1.append(a[j])
        b1.append(b[j])
        j=j+1
    name="zoomplot nr "
    nr=str(h)
    endung="a.pdf"
    plotname=name+nr+endung
    titel=name+nr
    plt.plot(a1,b1,'k-')
    plt.plot(a1,b1,'r*')
    plt.xlabel("Eingestellte Zeit in ns")
    plt.ylabel('relative Abweichung')
    plt.grid(True)
    plt.title(titel)
    plt.savefig(plotname)
    plt.close()
        
    h=h+1