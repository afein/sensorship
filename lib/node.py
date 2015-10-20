class Node(object):
    def __init__(self, id, sensors):
        self.id = id
        self.sensors = sensors

    def get_id(self):
        return self.id

    def get_sensors(self):
        return self.sensors

    def set_sensors(self, sensor):
        self.sensors.append(sensor)
