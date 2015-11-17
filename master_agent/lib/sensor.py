class Sensor(object):
    def __init__(self, type, units, value, timestamp):
        self.type = type
        self.units = units
        self.value = value
        self.timestamp = timestamp

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type

    def get_units(self):
        return self.units

    def set_units(self, units):
        self.units = units

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def get_timestamp(self):
        return self.timestamp

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp
