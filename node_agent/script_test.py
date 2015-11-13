import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from test_harness import *
from sensor import *

(container_id, port_bindings) = create_container('localhost', 'node_image', [1234, 1235])
print container_id, port_bindings

a0 = Sensor('GroveTemperature', 'A0')
d3 = Sensor('GroveButton', 'D3')

port1 = port_bindings.items()[0][1]
create_datapipe('localhost', 'localhost', port1, a0, 5)

port2 = port_bindings.items()[1][1]
create_datapipe('localhost', 'localhost', port2, d3, 6)


'''
d2 = Sensor('GroveTouch', 'D2')
d3 = Sensor('GroveButton', 'D3')

a0 = Sensor('GroveTemperature', 'A0')
a1 = Sensor('GroveLight', 'A1')
a2 = Sensor('GroveRotaryAngle', 'A2')

create_datapipe('localhost', 'localhost', 1234, d2, 2)
create_datapipe('localhost', 'localhost', 1235, d3, 2)

create_datapipe('localhost', 'localhost', 1236, a0, 2)
create_datapipe('localhost', 'localhost', 1237, a1, 2)
create_datapipe('localhost', 'localhost', 1238, a2, 2)
'''
