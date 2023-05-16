import tdc7201
import time
import plotext as plt
import numpy as np
import vxi11
import matplotlib.pyplot as plt

tdc = tdc7201.TDC7201()
tdc.initGPIO(enable=11, osc_enable=15, trig1=7, int1=29, trig2=None, int2=None, verbose=True, start=None, stop=None)
tdc.set_SPI_clock_speed(1250000)
tdc.on()
tdc.configure(meas_mode=2,num_stop=1, trig_falling=False, calibration2_periods=10)


instr=vxi11.Instrument("129.217.164.90")
instr.write("LAMP 0,3.3")
instr.write("LAMP 1,3.3")
instr.write("LAMP 2,3.3")
instr.write("LAMP 3,3.3")
instr.write("LAMP 4,3.3")
instr.write("DLAY 4,2,250e-9")
instr.write("TRAT 1e3")
befehl1="DLAY "
komma=","
zpotenz="e-12"
i=0
start=int(input("delta t in ps: "))

Delay="DISP 11,4"
flanke1="1"
flanke2="2"
flanke3="3"
flanke4="4"
times = []
x=int(input("Anzahl der Messungen: "))
t1="Eingestellt Zeit = "
t2=" ns"
t3=" mit "
t4=" Messungen Modus 2"
endung=".pdf"
ednung2=".txt"
pfad="histogramme/"
titel=t1+str(start*1e-3)+t2+t3+str(x)+t4
saveas=pfad+str(start*1e-3)+t2+endung
saveastxt=pfad+str(start*1e-3)+t2+endung
try:
    pck=befehl1 + flanke4 + komma + flanke2 + komma + str(start) + zpotenz
    instr.write(pck)
    instr.write(Delay)
    while i<1:
        status = tdc.measure(simulate=False)
        if status == 1:
            tdc.compute_tofs()
            times.append(tdc.tof1*1e12)
            if(len(times) % x == 0):

                titel=t1+str(start*1e-3)+t2+t3+str(x)+t4
                saveas=pfad+str(start*1e-3)+t2+endung
                saveastxt=pfad+str(round(start*1e-3,2))+t2+ednung2
                
                plt.hist(times, bins=100)
                plt.xlabel("Δt  /ns")
                plt.ylabel("Anzahl der Ereignisse")
                plt.title(titel)
                plt.savefig(saveas)
                plt.close('all')

                with open(saveastxt,"w") as temp_file:
                    for item in times:
                        temp_file.write("%s\n"% item)

                i=i+1
except KeyboardInterrupt:
    tdc.off()