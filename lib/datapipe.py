class Datapipe(object):
    def __init__(self, id, sensor):
        self.id = id
        self.sensor = sensor

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = self.id

    def get_sensor(self):
        return self.sensor

    def set_sensor(self, sensor):
        self.sensor = sensor
