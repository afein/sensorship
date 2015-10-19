import docker
from sensor_formatter import SensorDataFormatter

class VirtualNetworkManager(object):
    def __init__(self):
        pass

    def create_datapipe(self, type, host, port, sensor, interval):
        pass

    def delete_datapipe(self, type, host, port, sensor):
        pass

    def link(self, container, datapipe):
        pass
