from docker import Client
from docker.utils import kwargs_from_env

class DockerInterface(object):

    def __init__(self):
        self.client = Client(**kwargs_from_env(assert_hostname=False))

    def run_container(self, image, ports):
        # Pull the image if it's not present
        print "before pull"
        self.client.pull(image)
        print "after pull"

        port_bindings = {}
        for port in ports:
            port_bindings[port] = ('0.0.0.0',)

        container = self.client.create_container(
            image=image,
            ports=ports,
            host_config=self.client.create_host_config(port_bindings=port_bindings)
        )

        print container
        container_id = container.get("Id")
        
        self.client.start(container=container_id)

        print "Started"

        bindings = {}
        print "inspecting container"
        
        inspect_container = self.client.inspect_container(container_id)
        for k,v in inspect_container['NetworkSettings']['Ports'].iteritems():
            cport = int(k.split('/')[0])
            bindings[cport] = int(v[0]['HostPort'])
        print "finished inspecting"

        return (container_id, bindings)

    def delete_container(self, container):
        self.client.stop(container, timeout=0) 
        self.client.remove_container(container)

