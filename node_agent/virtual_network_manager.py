from sensor import *
import sensor_formatter

from threading import Lock
from threading import Timer
import sys
import socket

#from sensor_formatter import SensorDataFormatter

class Datapipe(object):

    def __init__(self, peripheral, host, port):
        self.peripheral = peripheral
        self.host = host
        self.port = port

    def __hash__(self):
        return hash((self.peripheral, self.host, self.port))

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
                   and self.__dict__ == other.__dict__

    def __str__(self):
        return '%s %s %s' % (self.peripheral, self.host, self.port)

class VirtualNetworkManager(object):

    def __init__(self, SDF):
        # Datapipe : interval (s) - negative indicates to remove
        self.datapipes = {}
        self.lock = Lock()
        self.SDF = SDF 

    def create_datapipe(self, peripheral, host, port, interval):
        d = Datapipe(peripheral, host, port)
        with self.lock:
            if d in self.datapipes.keys():
                raise Exception('Error create_datapipe: datapipe already exists!', str(d))
                sys.exit(1)

            self.datapipes[d] = interval

        self._poll(d) # start polling

    def delete_datapipe(self, peripheral, host, port):
        d = Datapipe(peripheral, host, port)
        with self.lock:
            if d not in self.datapipes.keys():
                raise Exception('Error delete_datapipe: datapipe does not exist!', str(d))
                sys.exit(1)

            self.datapipes.pop(d)

    def link(self, container, datapipe):
        # do nothing - port bindings take care of it
        pass

    def _poll(self, d):
        poll_again = True
        interval = 0
        with self.lock:
            if d not in self.datapipes.keys():
                poll_again = False 
            else:
                interval = self.datapipes[d]
        
        data = self.SDF.poll_peripheral(d.peripheral)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((d.host, d.port))
            s.send(data)
        finally:
            s.close()

        if poll_again:
            Timer(interval, self._poll, [d]).start()

