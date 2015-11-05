import time

from test_harness import *

import sys
sys.path.append('../dev') # TODO: project structure 
from sensor import *

(container_id, port_bindings) = create_container('localhost', 'node_image', [1234, 1235])
#print container_id, port_bindings

s1 = Sensor('grove_temperature', 'A0')
s2 = Sensor('grove_button', 'D3')

time.sleep(5)

port1 = port_bindings.items()[0][1]
create_datapipe('localhost', 'localhost', port1, s1, 1)

port2 = port_bindings.items()[1][1]
create_datapipe('localhost', 'localhost', port2, s2, 2)

#delete_container('localhost', container_id)
#print container_id
