import tdc7201
import time
import plotext as plt
import numpy as np
import vxi11
import matplotlib.pyplot as plt
import os

tdc = tdc7201.TDC7201()
tdc.initGPIO(enable=11, osc_enable=15, trig1=7, int1=29, trig2=None, int2=None, verbose=True, start=None, stop=None)
tdc.set_SPI_clock_speed(1250000)
tdc.on()
tdc.configure(meas_mode=1,num_stop=1, trig_falling=False, calibration2_periods=10)
tdc.write8(0x00,0x01)
print("Wert des CONFIG1 Bits: ",tdc.read8(0x00))


instr=vxi11.Instrument("129.217.164.90")
instr.write("LAMP 0,3.3")
instr.write("LAMP 1,3.3")
instr.write("LAMP 2,5")
instr.write("LAMP 3,3.3")
instr.write("LAMP 4,3.3")
instr.write("TRAT 1e3")
instr.write("DLAY 4,2,250e-9")


befehl1="DLAY "
Delay="DISP 11,4"
komma=","
zpotenz="e-9"
flanke1="1"
flanke2="2"
flanke3="3"
flanke4="4"
t1="Eingestellt Zeit = "
t2="ns"
t3=" mit "
t4=" Messungen Modus 1"
t5="ps"
t6="log"
endung=".pdf"
endung2=".txt"
pfad="histogramme/"
sl="/"
s="-"
at="@"


#start=int(input("Startzeit in ps: "))/1e3
#stop=int(input("Stopzeit in ps: "))/1e3
#step=int(input("Schrittweite in ps: "))/1e3
#x=int(input("Anzahl der Messungen pro Schritt:"))

start=7
stop=20
step=0.01
x=5000


ordnerpfad=pfad + str(round(start,2)) + s + str(round(stop,2)) + t2 + at + str(round(step*1e3,2)) + t5
if not os.path.exists(ordnerpfad):
    os.makedirs(ordnerpfad)


log=ordnerpfad+sl+t6+endung2
logdatei = open(log,'a')
time_string=time.strftime("%d-%m-%Y, %H:%M:%S")
startzeit=time.time()
logdatei.write("Start der Messung: ")
logdatei.write(time_string)
logdatei.write('\r\n')
logdatei.close()




i=0
times = []
count=0

titel=t1+str(start+i*step)+t2+t3+str(x)+t4
saveas=pfad+str(start+i*step)+t2+endung
saveastxt=pfad+str(start+i*step)+t2+endung
try:
    pck=befehl1 + flanke4 + komma + flanke2 + komma + str(start) + zpotenz
    instr.write(pck)
    instr.write(Delay)
    while i<=int((stop-start)/step):
        status = tdc.measure(simulate=False)
        if status == 1:
            CALIBRATION1=tdc.read24(0x1B)
            CALIBRATION2=tdc.read24(0x1C)
            TIME1=tdc.read24(0x10)
            CLOCK=8e6
            CALIBRATION_PERIODS=10
            calCount=(CALIBRATION2-CALIBRATION1)/(CALIBRATION_PERIODS-1)
            normalLSB=1/(calCount*CLOCK)
            TOF=(TIME1*normalLSB)-91.3 #ungefähre Kabellänge

            times.append(TOF*1e9)
            if(len(times) % x == 0):

                #titel=t1+str(start+i*step)+t2+t3+str(x)+t4
                #saveas=ordnerpfad+sl+str(start+i*step)+t2+endung
                saveastxt=ordnerpfad+sl+str(round(start+i*step,2))+t2+endung2
                
                #plt.hist(times, bins=100)
                #plt.xlabel("Δt  /ns")
                #plt.ylabel("Anzahl der Ereignisse")
                #plt.title(titel)
                #plt.savefig(saveas)
                #plt.close('all')

                with open(saveastxt,"w") as temp_file:
                    for item in times:
                        temp_file.write("%s\n"% item)

                wert=str(start+i*step)
                pck=befehl1 + flanke4 + komma + flanke2 + komma + wert + zpotenz
                instr.write(pck)
                instr.write(Delay)
                print(i," von ", int((stop-start)/step))
                times = []
                i=i+1
        count=count+1
    
    stopzeit=time.time()
    logdatei = open(log,'a')
    time_string=time.strftime("%d-%m-%Y, %H:%M:%S")
    logdatei.write("Ende der Messung: ")
    logdatei.write(time_string)
    logdatei.write('\r\n')
    logdatei.write("Dauer der Messung in s: ")
    logdatei.write(str(stopzeit-startzeit))
    logdatei.write('\r\n')
    logdatei.write("Messzyklen gesamt: ")
    logdatei.write(str(count))
    logdatei.write('\r\n')
    logdatei.write("Messzyklen erfolgreich: ")
    logdatei.write(str(i))
    logdatei.write('\r\n')
    logdatei.close()
except KeyboardInterrupt:
    tdc.off()
    stopzeit=time.time()
    logdatei = open(log,'a')
    time_string=time.strftime("%d-%m-%Y, %H:%M:%S")
    logdatei.write("Ende der Messung: ")
    logdatei.write(time_string)
    logdatei.write('\r\n')
    logdatei.write("Dauer der Messung in s: ")
    logdatei.write(str(stopzeit-startzeit))
    logdatei.write('\r\n')
    logdatei.write("Messzyklen gesamt: ")
    logdatei.write(str(count))
    logdatei.write('\r\n')
    logdatei.write("Messzyklen erfolgreich: ")
    logdatei.write(str(i*x))
    logdatei.write('\r\n')
    logdatei.close()
