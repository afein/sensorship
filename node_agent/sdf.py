import json
import requests

from sets import Set
from threading import Lock
from threading import Timer
from fractions import gcd


class Endpoint(object):

    def __init__(self, host, port, interval):
        self.host = host
        self.port = port
        self.interval = interval
        self.accumulated = 0

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
                    and self.host == other.host  \
                    and self.port == other.port

    def __hash__(self):
        return hash((self.host, self.port))

    def __repr__(self):
        return str(self.__dict__)


class Sensorpipe(object):

    def __init__(self, host, sensor):
        self.host = host 
        self.sensor = sensor
        self.lock = Lock()
        self.endpoints = Set([])
        self.tick = -1          # in seconds (-1 turns off)
        self.MIN_TICK = 0.100   # for now, min tick interval set to 100ms

    def add_endpoint(self, endpoint):
        prev_len = None
        with self.lock:
            prev_len = len(self.endpoints)
            assert endpoint not in self.endpoints, '%r %r %r' % (self.host, self.sensor, endpoint)
            self.endpoints.add(endpoint)
            self._update_tick()

        if prev_len == 0:
            self._tick()

    def delete_endpoint(self, endpoint):
        with self.lock:
            assert endpoint in self.endpoints, '%r %r %r' % (self.host, self.sensor, endpoint)
            self.endpoints.remove(endpoint)
            self._update_tick()

    # intervals are in seconds
    # aim to support interval resolution of 100 ms (rounded down)
    # UI should impose contraints of minimum interval and resolution of 100 ms
    def _gcd(self, intervals):
        scaled_intervals = [int(i*10) for i in intervals]
        scaled_gcd = reduce(gcd, scaled_intervals)
        my_gcd = float(scaled_gcd)/10
        assert my_gcd > self.MIN_TICK, '%r %r %r' % (self.host, self.sensor, my_gcd)

        return my_gcd

    def _update_tick(self): # only invoke when locked
        if len(self.endpoints) > 0:
            intervals = [e.interval for e in self.endpoints]
            self.tick = self._gcd(intervals)
        else:
            self.tick = -1

    def _tick(self):
        current_len = None
        current_tick = None
        receiving_ports = []

        with self.lock:
            current_len = len(self.endpoints)
            current_tick = self.tick
            for endpoint in self.endpoints:
                endpoint.accumulated += current_tick
                if endpoint.accumulated >= endpoint.interval:
                    remainder = endpoint.accumulated - endpoint.interval
                    endpoint.accumulated = remainder
                    receiving_ports.append(endpoint.port)

        if current_len > 0:
            if len(receiving_ports) > 0:
                payload = json.dumps({'ports' : receiving_ports, 'host' : self.host, 'sensor' : self.sensor, 'tick' : current_tick})
                try:
                    r = requests.post("http://%s:5000/sensor_data" % self.host, data=payload) # TODO: timeout?
                except Exception as e:
                    print e

            Timer(current_tick, self._tick, []).start()


class Datapipe(object):

    def __init__(self, host):
        self.host = host
        self.lock = Lock()
        self.sensorpipes = {} # {Sensor : Sensorpipe}
        # TODO: sensor must be hashable

    def add_sensorpipe_endpoint(self, sensor, endpoint):
        sensorpipe = None
        with self.lock:
            if sensor in self.sensorpipes.keys():
                sensorpipe = self.sensorpipes[sensor]
            else:
                sensorpipe = Sensorpipe(self.host, sensor)
                self.sensorpipes[sensor] = sensorpipe

        sensorpipe.add_endpoint(endpoint)

    def delete_sensorpipe_endpoint(self, sensor, endpoint):
        sensorpipe = None
        with self.lock:
            assert sensor in self.sensorpipes.keys(), '%r %r' % (self.host, sensor)
            sensorpipe = self.sensorpipes[sensor]
        
        sensorpipe.delete_endpoint(endpoint)


class SensorDataFormatter(object):

    def __init__(self):
        self.lock = Lock()
        self.datapipes = {} # {host : Datapipe}

    def subscribe(self, host, port, sensor, interval):
        datapipe = None
        with self.lock:
            if host in self.datapipes.keys():
                datapipe = self.datapipes[host]
            else:
                datapipe = Datapipe(host)
                self.datapipes[host] = datapipe

        endpoint = Endpoint(host, port, interval)
        datapipe.add_sensorpipe_endpoint(sensor, endpoint)

    def unsubscribe(self, host, port, sensor):
        datapipe = None
        with self.lock:
            assert host in self.datapipes.keys(), '%r' % host
            datapipe = self.datapipes[host]

        endpoint = Endpoint(host, port, 0)
        datapipe.delete_sensorpipe_endpoint(sensor, endpoint)

    def register_sensor(sensor, pin):
        pass

