import json
import socket

from fractions import gcd
from sets import Set
from threading import Lock
from threading import Timer

from sensor import *


class Endpoint(object):

    def __init__(self, host, port, interval):
        self.host = host
        self.port = port
        self.interval = interval # in seconds
        self.accumulated = 0     # in seconds

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
                   and self.host == other.host \
                   and self.port == other.port

    def __hash__(self):
        return hash((self.host, self.port))

    def __str__(self):
        return  json.dumps({'host' : self.host, 'port' : self.port, 'interval' : self.interval})


class Datapipe(object):

    def __init__(self, poll_func):
        self.poll_func = poll_func
        self.endpoints = Set([])
        self.lock = Lock()
        self.tick = -1          # in seconds (-1 turns off) 
        self.MIN_TICK = 0.100   # for now, min tick interval set to 100 ms

    def add_endpoint(self, endpoint):
        prev_len = None 
        with self.lock:
            prev_len = len(self.endpoints) 
            if endpoint not in self.endpoints:
                self.endpoints.add(endpoint)
                self._update_tick()
            else:
                raise Exception('Error add_endpoint: endpoint already exists', endpoint)

        if prev_len == 0:
            self._tick()

    def delete_endpoint(self, endpoint):
        with self.lock:
            if endpoint in self.endpoints:
                self.endpoints.remove(endpoint)
                self._update_tick()
            else:
                raise Exception('Error delete_endpoint: endpoint does not exist', endpoint)

    # interval are in seconds
    # aim to support interval resolution of 100 ms (rounded down)
    # UI should impose contraints of minimum interval and resolution of 100 ms
    def _gcd(self, interval_list):
        scaled_intervals = [int(i*10) for i in interval_list]
        scaled_gcd = reduce(gcd, scaled_intervals)
        my_gcd = float(scaled_gcd) / 10

        if my_gcd < self.MIN_TICK:
            raise Exception('Error _gcd: computed gcd below minimum', my_gcd)
        
        return my_gcd

    def _update_tick(self): # only invoke when locked
        if len(self.endpoints) > 0:
            interval_list = [e.interval for e in self.endpoints]
            self.tick = self._gcd(interval_list)
        else:
            self.tick = -1
                
    def _tick(self):
        current_len = None
        current_tick = None
        due_endpoints = []

        with self.lock:
            current_len = len(self.endpoints)
            current_tick = self.tick
            if current_len > 0:
                for endpoint in self.endpoints:
                    endpoint.accumulated += current_tick 
                    if endpoint.accumulated >= endpoint.interval:
                        remainder = endpoint.accumulated - endpoint.interval
                        endpoint.accumulated = remainder 
                        due_endpoints.append(endpoint)

        if current_len > 0:
            data = self.poll_func() # TODO
            for de in due_endpoints:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    s.connect((de.host, de.port))
                    s.send(data)
                finally:
                    s.close()

            Timer(current_tick, self._tick, []).start()


class VirtualNetworkManager(object):

    def __init__(self, SDF):
        self.SDF = SDF
        self.datapipes = {} # {peripheral : datapipe}
        self.lock = Lock()
        self.SDF = SDF

    def create_datapipe(self, peripheral, host, port, interval):
        endpoint = Endpoint(host, port, interval)
        datapipe = None
        with self.lock:
            if peripheral not in self.datapipes.keys():
                poll_func = self.SDF.get_poll_func(peripheral)
                datapipe = Datapipe(poll_func)
                self.datapipes[peripheral] = datapipe
            else:
                datapipe = self.datapipes[peripheral]

        datapipe.add_endpoint(endpoint)

    def delete_datapipe(self, peripheral, host, port):
        cmp_endpoint = Endpoint(host, port, 0)
        datapipe = None
        with self.lock:
            if peripheral in self.datapipes.keys():
                datapipe = self.datapipes[peripheral]
            else:
                raise Exception('Error delete_datapipe: peripheral does not exist', str(peripheral))

        datapipe.delete_endpoint(cmp_endpoint)

    def link(self, container, datapipe):
        # do nothing - port bindings take care of it
        pass

