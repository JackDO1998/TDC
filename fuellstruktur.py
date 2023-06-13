from multiprocessing import Process, Queue
import channel_access.common as ca
import channel_access.server as cas
import tdc7201
import time
import random




def read_spi(q):
    t=0
    while t <= 6000:
        q.put(random.uniform(0,100))
        t=t+1
        time.sleep(0.1)
        


if __name__ == '__main__':
    q = Queue()
    p = Process(target=read_spi, args=(q,))
    p.start()

    with cas.Server() as server:
        pv = server.createPV('GAS-buckets', ca.Type.FLOAT, count=192)

        values = []
        while True:
            values.append(q.get())
            if len(values) > 192:
                buckets = values[:192]
                values = []
                pv.value=buckets

    p.join()
 