from multiprocessing import Process, Queue
import channel_access.common as ca
import channel_access.server as cas
import tdc7201
import time
import random
import matplotlib.pyplot as plt





def read_spi(q):
    t=0
    while t <= 600000:
        a=2*random.uniform(0,96) + random.gauss(18,1)/1000
        q.put(a)
        t=t+1
        time.sleep(0.001)
        


if __name__ == '__main__':
    q = Queue()
    p = Process(target=read_spi, args=(q,))
    p.start()

    with cas.Server() as server:
        pv = server.createPV('GAS-buckets', ca.Type.FLOAT, count=192)
        print(len(pv.value))

        values = []
        while True:
            values.append(q.get())
            if len(values) % 100 == 0:
                buckets=plt.hist(values, bins=192)
                print(buckets)
                print(len(buckets))
                pv.value =buckets 
                
            if len(values) > 10000:
                j=0
                while j <= 100:
                    del values[j]
                    j+=1

    p.join()
 