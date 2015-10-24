from docker import Client
from docker.utils import kwargs_from_env

client = Client(**kwargs_from_env(assert_hostname=False))

''' Master, slave interactions

def master_run_container(image, sensor_ports={'s1' : 1234, 's2' : 1235}):
    # scheduler determines node
    # slave runs container - returns port bindings 
    # create datapipes 
    # return jobid

def master_stop_container(jobid):
    # check cluster state for job
    # delete datapipes 
    # delete container
'''

# TODO: pulling images
def run_container(image='node_image'):
    # get exposed ports
    ports = []
    inspect_image = client.inspect_image(image)
    for k in inspect_image['ContainerConfig']['ExposedPorts']:
        ports.append(k.split('/')[0])

    # create container with automatic port-bindings
    port_bindings = {}
    for port in ports:
        port_bindings[port] = ('0.0.0.0',)

    container_id = client.create_container(
        image=image,
        name='test',
        ports=ports,
        host_config=client.create_host_config(port_bindings=port_bindings)
    )['Id']
    
    print container_id
    client.start(container_id)

    # return port-bindings
    bindings = {}
    inspect_container = client.inspect_container('test')
    for k,v in inspect_container['NetworkSettings']['Ports'].iteritems():
        cport = k.split('/')[0]
        bindings[cport] = v[0]['HostPort']

    print bindings
    return (container_id, bindings)

def del_container(container='test'):
    client.stop(container) 
    client.remove_container(container)

