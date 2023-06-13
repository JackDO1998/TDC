import channel_access.common as ca
import channel_access.client as cac
import time

while True:
    with cas.Client() as client:
        pv =  client.createPV('GAS-buckets', monitor=False, initialize=cac.InitData.NONE)
        print(pv.data)
        time.sleep(1)
        