import vxi11
import time
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
flanke5="5"
flanke6="6"
flanke7="7"
flanke8="8"
flanke9="9"
flanke10="10"


while i<=(stop-start)/step:
    wert=str(start+i*step)
    pck=befehl1 + flanke4 + komma + flanke2 + komma + wert + zpotenz
    instr.write(pck)
    instr.write(Delay)
    time.sleep(1)
    i=i+1
