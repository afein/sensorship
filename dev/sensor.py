import json
import rpi
from time import gmtime, strftime

class Sensor(object):

    def __init__(self, device, port):
        assert device in rpi.devices.keys()
        sensor_type = rpi.devices[device]['sensor_type']
        assert sensor_type in rpi.ports.keys()
        assert port in rpi.ports[sensor_type].keys()
        self.device = device
        self.port = port
        self.pin = rpi.ports[sensor_type][port]
        self.units = rpi.devices[device]['units']

    def __eq__(self, other):
        return isinstance(other, self.__class__)             \
                   and self.device == other.device           \
                   and self.port == other.port

    def __hash__(self):
        return hash((self.device, self.port))

    def __repr__(self):
        return json.dumps({'device' : self.device, 'port' : self.port}) 


class SensorReading(object):

    def __init__(self, sensor, value):
        self.sensor = sensor
        self.value = value
        self.time = strftime("%a, %d %b %Y %X +0000", gmtime()) 

    def __repr__(self):
        return json.dumps({'sensor' : '%r' % self.sensor, 'value' : self.value, 'units' : self.sensor.units, 'time' : self.time})

