class Datapipe(object):
    def __init__(self, sensor, local_node, remote_node, remote_port):
        self.sensor = sensor
        self.local_node = local_node
        self.remote_node = remote_node
        self.remote_port = remote_port

    def get_sensor(self):
        return self.sensor

    def set_sensor(self, sensor):
        self.sensor = sensor

    def get_local_node(self):
        return self.local_node

    def set_local_node(self, local_node):
        self.local_node = local_node

    def get_remote_node(self):
        return self.remote_node

    def set_remote_node(self, remote_node):
        self.remote_node = remote_node

    def get_remote_port(self):
        return self.remote_port

    def set_remote_port(self, remote_port):
        self.remote_port = remote_port
