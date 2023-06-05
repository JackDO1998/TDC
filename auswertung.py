# -*- coding: utf-8 -*-
"""
Created on Mon May 15 23:15:53 2023

@author: janga
"""
import matplotlib.pyplot as plt
import numpy as np
a1=np.loadtxt('D:/OneDrive/Dokumente/Bachelorarbeit/MittelwertzoomplotsLED/7-400ns/mittelwerteLED.txt', usecols=[0], dtype=float)
b1=np.loadtxt('D:/OneDrive/Dokumente/Bachelorarbeit/MittelwertzoomplotsLED/7-400ns/mittelwerteLED.txt', usecols=[1], dtype=float)
c1=b1-a1
a2=np.loadtxt('D:/OneDrive/Dokumente/Bachelorarbeit/MittelwertzoomplotsLED/7-50ns/mittelwerteLED.txt', usecols=[0], dtype=float)
b2=np.loadtxt('D:/OneDrive/Dokumente/Bachelorarbeit/MittelwertzoomplotsLED/7-50ns/mittelwerteLED.txt', usecols=[1], dtype=float)
c2=b2-a2
a3=np.loadtxt('D:/OneDrive/Dokumente/Bachelorarbeit/MittelwertzoomplotsLED/7-50ns@250ps/mittelwerteLED.txt', usecols=[0], dtype=float)
b3=np.loadtxt('D:/OneDrive/Dokumente/Bachelorarbeit/MittelwertzoomplotsLED/7-50ns@250ps/mittelwerteLED.txt', usecols=[1], dtype=float)
c3=b3-a3
a=[]
c=[]
z=0
while z <= len(a1)-1:
    a.append(a1[z])
    c.append(c1[z])
    z=z+1
plt.plot(a,c,'r*',label='250 ps')
plt.plot(a2,c2,'b*',label='100 ps')
plt.plot(a3,c3,'g*',label='250 ps')
plt.grid(True)
plt.legend(loc='best')
plt.xlabel("Eingestellte Zeit in ns")
plt.ylabel('Abweichung')
plt.title('Gesamtplot')
plt.savefig('D:/OneDrive/Dokumente/Bachelorarbeit/MittelwertzoomplotsLED/7-400ns/Gesamtplot kombiniert 2 norm.pdf')
plt.close()

#j=0
#h=1
#while h<=25:
#    a1=[]
#    b1=[]
#    while j<=(h*100)-1:
#        a1.append(a[j])
#        b1.append(c[j])
#        j=j+1
#    name="D:/OneDrive/Dokumente/Bachelorarbeit/MittelwertzoomplotsLED/7-400ns/zoomplot nr "
#   nr=str(h)
#    endung="a.pdf"
#    plotname=name+nr+endung
#    titel=name+nr
#    plt.plot(a1,b1,'k-')
#    plt.plot(a1,b1,'r*')
#    plt.xlabel("Eingestellte Zeit in ns")
#   plt.ylabel('relative Abweichung')
#    plt.grid(True)
#    plt.title(titel)
    #plt.savefig(plotname)
#    plt.close()
        
#    h=h+1
