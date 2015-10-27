from enum import Enum
import json


class SensorType(Enum):
    # the sensors in the Grove Kit
    grove_button = 1
    grove_tilt_switch = 2
    grove_rotary_angle = 3
    grove_temperature = 4


class SensorInterface(Enum):
    digital = 1
    analog = 2
    # interrupt = 3 ? for button/pir


class Sensor(object):

    def __init__(self, sensor_type, sensor_interface):
        self.sensor_type = sensor_type
        self.sensor_interface = sensor_interface

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
                   and self.sensor_type == other.sensor_type \
                   and self.sensor_interface == other.sensor_interface

    def __hash__(self):
        return hash((self.sensor_type, self.sensor_interface))

    def __str__(self):
        return json.dumps({'sensor_type' : self.sensor_type.name, 'sensor_interface' : self.sensor_interface.name}) 


class Peripheral(object):

    def __init__(self, sensor, pin):
        self.sensor = sensor
        self.pin = pin

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
                   and self.sensor == other.sensor \
                   and self.pin == other.pin

    def __hash__(self):
        return hash((self.sensor, self.pin))

    def __str__(self):
        return json.dumps({'sensor' : str(self.sensor), 'pin' : self.pin})


class SensorReading(object):

    def __init__(self, sensor, value, units, timestamp):
        self.sensor = sensor
        self.value = value
        self.units = units
        self.timestamp = timestamp

    def __str__(self):
        return json.dumps({'sensor' : str(self.sensor), 'value' : self.value, 'units' : self.units, 'timestamp' : self.timestamp})

