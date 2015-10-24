from threading import Lock
from threading import Timer
import sys

#from sensor_formatter import SensorDataFormatter

class Datapipe(object):

    def __init__(self, sensor, host, port):
        self.sensor = sensor
        self.host = host
        self.port = port

    def __hash__(self):
        return hash((self.sensor, self.host, self.port))

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
                   and self.__dict__ == other.__dict__

    def __str__(self):
        return '%s %s %s' % (self.sensor, self.host, self.port)

class VirtualNetworkManager(object):

    def __init__(self):
        # Datapipe : interval (s) - negative indicates to remove
        self.datapipes = {}
        self.lock = Lock()

    def create_datapipe(self, sensor, host, port, interval):
        d = Datapipe(sensor, host, port)
        with self.lock:
            if d in self.datapipes.keys():
                raise Exception('Error create_datapipe: datapipe already exists!', str(d))
                sys.exit(1)

            self.datapipes[d] = interval

        self.poll(d) # start polling

    def delete_datapipe(self, sensor, host, port):
        d = Datapipe(sensor, host, port)
        with self.lock:
            if d not in self.datapipes.keys():
                raise Exception('Error delete_datapipe: datapipe does not exist!', str(d))
                sys.exit(1)

            self.datapipes.pop(d)

    def link(self, container, datapipe):
        # do nothing - port bindings take care of it
        pass

    def poll(self, d):
        poll_again = True
        interval = 0
        with self.lock:
            if d not in self.datapipes.keys():
                poll_again = False 
            else:
                interval = self.datapipes[d]


        # TODO: poll sensor, send data
        # print 'poll %s %s %s %s' % (d.sensor, d.host, d.port, interval)
        print d

        if poll_again:
            Timer(interval, self.poll, [d]).start()

