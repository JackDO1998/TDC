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
tdc.configure(meas_mode=2,num_stop=4, trig_falling=False, calibration2_periods=10, clock_cntr_stop = 120)
tdc.write8(0x01,0x43)
tdc.write8(0x00,0x03)
print(tdc.read8(0x01))
print(tdc.read8(0x00))
CLOCK=8e6
CALIBRATION_PERIODS=10
titel="Burstmode "
saveas="Burstmode.pdf"
saveastxt="Burstmode.txt"
x=4000
times=[]
i=0
try:
    while i==0:
        tdc.write8(0x00,0x03)
        time.sleep(0.1)
        status = 1#tdc.measure(simulate=False)
        if status == 1:
            print("Datensatz vorhanden")
            CALIBRATION1=tdc.read24(0x1B)
            CALIBRATION2=tdc.read24(0x1C)
            TIME1=tdc.read24(0x10)
            TIME2=tdc.read24(0x12)
            TIME3=tdc.read24(0x14)
            TIME4=tdc.read24(0x16)
            TIME5=tdc.read24(0x18)
            COUNT1=tdc.read24(0x11)
            COUNT2=tdc.read24(0x13)
            COUNT3=tdc.read24(0x15)
            COUNT4=tdc.read24(0x17)
            calCount=(CALIBRATION2-CALIBRATION1)/(CALIBRATION_PERIODS-1)
            normalLSB=1/(calCount*CLOCK)
            
            TOF1=TIME1*normalLSB + COUNT1/CLOCK - (TIME2*normalLSB)
            TOF2=TIME2*normalLSB + COUNT2/CLOCK - (TIME3*normalLSB)
            TOF3=TIME3*normalLSB + COUNT3/CLOCK - (TIME4*normalLSB)
            TOF4=TIME4*normalLSB + COUNT4/CLOCK - (TIME5*normalLSB)

            print(TOF1)
            print(TOF2)
            print(TOF3)
            print(TOF4)

            times.append(TOF1*1e9)
            times.append(TOF2*1e9)
            times.append(TOF3*1e9)
            times.append(TOF4*1e9)

            if(len(times) % x == 0):
                plt.hist(times, bins=1000)
                plt.xlabel("Δt  /ns")
                plt.ylabel("Anzahl der Ereignisse")
                plt.title(titel)
                plt.savefig(saveas)
                plt.close('all')

                with open(saveastxt,"w") as temp_file:
                    for item in times:
                        temp_file.write("%s\n"% item)
                i=1 

except KeyboardInterrupt:
    tdc.off()