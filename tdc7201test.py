import tdc7201
import time
import plotext as plt
import numpy as np
import vxi11
import matplotlib.pyplot as plt
tdc = tdc7201.TDC7201()
tdc.initGPIO(enable=12, osc_enable=16, trig1=7, int1=37, trig2=None, int2=None, verbose=True, start=None, stop=None)
tdc.set_SPI_clock_speed(1250000)
tdc.on()
tdc.configure(meas_mode=2,num_stop=1, trig_falling=False)

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
start=250
stop=800
step=10e-3
Delay="DISP 11,4"
flanke1="1"
flanke2="2"
flanke3="3"
flanke4="4"
times = []
t1="Eingestellt Zeit = "
t2=" ns"
endung=".pdf"
pfad="histogramme/"
titel=t1+str(i)+t2
saveas=pfad+str(i)+t2+endung
try:
    while i<=(stop-start)/step:
        status = tdc.measure(simulate=False)
        if status == 1:
            tdc.compute_tofs()
            times.append(tdc.tof1*1e9)
            if(len(times) % 5000 == 0):
                plt.hist(times, bins=100)
                plt.xlabel('Δt / ns')
                plt.show()
                plt.clf()

                plt.hist(times, bins=100)
                plt.xlabel("Δt  /ns")
                plt.ylabel("Anzahl der Ereignisse")
                plt.title(titel)
                plt.savefig(saveas)

                wert=str(start+i*step)
                pck=befehl1 + flanke4 + komma + flanke2 + komma + wert + zpotenz
                instr.write(pck)
                instr.write(Delay)
                print(i," von ", (stop-start)/step)
                times = []
                i=i+1
except KeyboardInterrupt:
    tdc.off()
