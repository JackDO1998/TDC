import multiprocessing

from multiprocessing import Process, Queue
import channel_access.common as ca
import channel_access.server as cas

def read_spi(q):
    value=0
    while True:
        value = value + 1
        q.put(value)

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
 