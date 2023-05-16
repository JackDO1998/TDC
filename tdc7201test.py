import tdc7201
import plotext as plt
import vxi11
import matplotlib.pyplot as plt
import time


tdc = tdc7201.TDC7201()
tdc.initGPIO(enable=11, osc_enable=15, trig1=7, int1=29, trig2=None, int2=None, verbose=True, start=None, stop=None)
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
zpotenz="e-12"
Delay="DISP 11,4"
flanke1="1"
flanke2="2"
flanke3="3"
flanke4="4"
t1="Eingestellt Zeit = "
t2=" ps"
t3=" mit "
t4=" Messungen Modus 2"
t5="ps"
t6="log"
endung=".pdf"
endung2=".txt"
pfad="histogramme/"
sl="/"
s="-"
at="@"


start=int(input("Startzeit in ps: "))
stop=int(input("Stopzeit in ps: "))
step=int(input("Schrittweite in ps: "))
x=int(input("Anzahl der Messungen pro Schritt: "))

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
    while i<=(stop-start)/step:
        status = tdc.measure(simulate=False)
        if status == 1:
            tdc.compute_tofs()
            times.append(tdc.tof1*1e12)
            if(len(times) % x == 0):
                
                titel=t1+str(start+i*step)+t2+t3+str(x)+t4
                saveas=pfad+str(start+i*step)+t2+endung
                saveastxt=pfad+str(start+i*step)+t2+endung2
                
                plt.hist(times, bins=100)
                plt.xlabel("Δt  /ps")
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
        count=count+1
except KeyboardInterrupt:
    tdc.off()
    stopzeit=time.time()
    logdatei = open(log,'a')
    time_string=time.strftime("%d-%m-%Y, %H:%M:%S")
    logdatei.write("Ende der Messung: ")
    logdatei.write('\r\n')
    logdatei.write(time_string)
    logdatei.write("Dauer der Messung in s: ")
    logdatei.write(stopzeit-startzeit)
    logdatei.write('\r\n')
    logdatei.write("Messzyklen gesamt: ")
    logdatei.write(count)
    logdatei.write("Messzyklen erfolgreich: ")
    logdatei.write(i)
    logdatei.write('\r\n')
    logdatei.close()
