from docker_interface import *
from sensor import *
from sensor_formatter import *
from virtual_network_manager import *

import time

(container_id, bindings) = run_container()

sensor1 = Sensor(SensorType.grove_temperature, SensorInterface.analog)
sensor2 = Sensor(SensorType.grove_tilt_switch, SensorInterface.digital)

peripheral1 = Peripheral(sensor1, 0)
peripheral2 = Peripheral(sensor2, 3)

sdf = SensorDataFormatter()
sdf.register_sensor(peripheral1.sensor, peripheral1.pin)
sdf.register_sensor(peripheral2.sensor, peripheral2.pin)

vnm = VirtualNetworkManager(sdf)
MACHINE_HOST = '192.168.99.100'
print bindings.items()
print bindings.items()[0]
print bindings.items()[1]

time.sleep(5)

vnm.create_datapipe(peripheral1, MACHINE_HOST, bindings.items()[0][1], 5)
vnm.create_datapipe(peripheral2, MACHINE_HOST, bindings.items()[1][1], 3)
