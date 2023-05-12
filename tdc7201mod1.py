import tdc7201
import time
import plotext as plt
import numpy as np
import vxi11
import matplotlib.pyplot as plt
import json
tdc = tdc7201.TDC7201()
tdc.initGPIO(enable=11, osc_enable=15, trig1=7, int1=29, trig2=None, int2=None, verbose=True, start=None, stop=None)
tdc.set_SPI_clock_speed(1250000)
tdc.on()
tdc.configure(meas_mode=1,num_stop=1, trig_falling=False, calibration2_periods=10)
tdc.write8(0x00,0x01)
print(tdc.read8(0x00))

instr=vxi11.Instrument("129.217.164.90")
instr.write("LAMP 0,3.3")
instr.write("LAMP 1,3.3")
instr.write("LAMP 2,3.3")
instr.write("LAMP 3,3.3")
instr.write("LAMP 4,3.3")
instr.write("DLAY 4,2,250e-9")
befehl1="DLAY "
komma=","
zpotenz="e-9"
i=0
start=int(input("Startzeit in ns: "))
stop=int(input("Stopzeit in ns: "))
step=int(input("Schrittweite in ps: "))/1e3
Delay="DISP 11,4"
flanke1="1"
flanke2="2"
flanke3="3"
flanke4="4"
times = []
x=5000
t1="Eingestellt Zeit = "
t2=" ns"
t3=" mit "
t4=" Messungen Modus 1"
endung=".pdf"
ednung2=".txt"
pfad="histogramme/"
titel=t1+str(start+i*step)+t2+t3+str(x)+t4
saveas=pfad+str(start+i*step)+t2+endung
saveastxt=pfad+str(start+i*step)+t2+endung
try:
    pck=befehl1 + flanke4 + komma + flanke2 + komma + str(start) + zpotenz
    instr.write(pck)
    while i<=(stop-start)/step:
        status = tdc.measure(simulate=False)
        if status == 1:
            CALIBRATION1=tdc.read24(0x1B)
            CALIBRATION2=tdc.read24(0x1C)
            TIME1=tdc.read24(0x10)
            CLOCK=8e6
            CALIBRATION_PERIODS=10
            calCount=(CALIBRATION2-CALIBRATION1)/(CALIBRATION_PERIODS-1)
            normalLSB=1/(calCount*CLOCK)
            TOF=TIME1*normalLSB

            times.append(TOF*1e9)
            if(len(times) % x == 0):

                titel=t1+str(start+i*step)+t2+t3+str(x)+t4
                saveas=pfad+str(start+i*step)+t2+endung
                saveastxt=pfad+str(start+i*step)+t2+ednung2
                
                plt.hist(times, bins=100)
                plt.xlabel("Δt  /ns")
                plt.ylabel("Anzahl der Ereignisse")
                plt.title(titel)
                plt.savefig(saveas)
                plt.close('all')

                with open(saveastxt,"w") as temp_file:
                    for item in times:
                        temp_file.write("%s\n"% item)

                wert=str(start+i*step)
                pck=befehl1 + flanke4 + komma + flanke2 + komma + wert + zpotenz
                instr.write(pck)
                instr.write(Delay)
                print(i," von ", (stop-start)/step)
                times = []
                i=i+1
except KeyboardInterrupt:
    tdc.off()
