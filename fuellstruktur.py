from multiprocessing import Process, Queue
import channel_access.common as ca
import channel_access.server as cas
import tdc7201


tdc = tdc7201.TDC7201()
tdc.initGPIO(enable=11, osc_enable=15, trig1=7, int1=29, trig2=None, int2=None, verbose=True, start=None, stop=None)
tdc.set_SPI_clock_speed(1250000)
tdc.on()
tdc.configure(meas_mode=1,num_stop=1, trig_falling=False, calibration2_periods=10)
tdc.write8(0x00,0x01)

def read_spi(q):
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
    
        q.put(TOF)

if __name__ == '__main__':
    q = Queue()
    p = Process(target=read_spi, args=(q,))
    p.start()

    with cas.Server() as server:
        pv = server.createPV('GAS-buckets', ca.Type.FLOAT, count=192)

        values = []
        while True:
            values.append(q.get())
            if len(values) > 8000:
                buckets = values[:192]
                values = []
                pv.value=buckets

    p.join()
 