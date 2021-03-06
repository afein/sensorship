import socket
import fcntl
import struct

class Node(object):
    def __init__(self, sensors, cpu, memory)
        self.sensors = []
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip = ipaddr = socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])
        self.cpu = None
        self.memory = None
        self.healthy = True

    def get_sensors(self):
        return self.sensors

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    def get_cpu(self):
        return self.cpu

    def set_cpu(self, cpu):
        self.cpu = cpu

    def get_memory(self):
        return self.memory

    def set_memory(self, memory):
        self.memory = memory

    def is_healthy(self):
        return self.healthy

    def set_healthy(self, is_healthy):
        self.healthy = is_healthy
