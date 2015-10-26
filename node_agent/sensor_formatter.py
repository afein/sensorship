from sensor import *
#import grovepi import *

import sys
import json


# for Raspberry Pi Grove Kit
# 7 digital ports (2-8)
# 3 analog (0-2)
class SensorDataFormatter(object):
    def __init__(self):
        self.peripherals = {}
        self.digital_ports = [2, 3, 4, 5, 6, 7, 8]
        self.analog_ports = [0, 1, 2]

    def subscribe(self, sensor, datapipe, interval):
        pass

    def unsubscribe(self, sensor, datapipe):
        pass

    def poll_peripheral(self, peripheral):
        return str(peripheral)

    def register_sensor(self, sensor, pin):
        p = Peripheral(sensor, pin)
        
        if self._validate_peripheral(p):
            self._set_peripheral(p)

    def _validate_peripheral(self, p):
        digital = p.sensor.sensor_interface == SensorInterface.digital
        ret = True
        if digital and p.pin not in self.digital_ports:
            raise Exception('Error _validate_peripheral: ', str(p))
            ret = False
        elif not digital and p.pin not in self.analog_ports:
            raise Exception('Error _validate_peripheral: ', str(p))
            ret = False

        return ret

    def _peripheral_key(self, p):
        key = '%s%d' % ('DIGITAL' if p.sensor.sensor_interface == SensorInterface.digital else 'ANALOG', p.pin)
        return key

    def _get_peripheral(self, p):
        key = self._peripheral_key(p)
        ret = None
        if key in self.peripherals.keys():
            ret = self.peripherals[key]

        return ret
    
    def _set_peripheral(self, p):
        key = self._peripheral_key(p) 
        if self._get_peripheral(p):
            raise Exception('Error _set_peripheral: ', str(p))

        self.peripherals[key] = p
        
