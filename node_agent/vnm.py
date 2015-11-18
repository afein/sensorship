
from threading import Thread
from sdf import SensorDataFormatter

class VirtualNetworkManager(object):

    def __init__(self, sdf):
        self.sdf = sdf

    # remote datapipe implemented as rest endpoint to arbitrate received data
    def create_datapipe(self, remote, host, port, sensor, interval):
        Thread(target=self.sdf.subscribe, args=(host, port, sensor, interval)).start()

    def delete_datapipe(self, remote, host, port, sensor):
        Thread(target=self.sdf.unsubscribe, args=(host, port, sensor)).start()
