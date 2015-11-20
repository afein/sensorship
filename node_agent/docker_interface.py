from docker import Client
from docker.utils import kwargs_from_env

class DockerInterface(object):

    def __init__(self):
        self.client = Client(**kwargs_from_env(assert_hostname=False))

    def run_container(self, image, ports):
        self.client.pull(image)
        print 'pulled image', image

        port_bindings = {}
        for port in ports:
            port_bindings[port] = ('0.0.0.0',)

        container = self.client.create_container(
            image=image,
            ports=ports,
            host_config=self.client.create_host_config(port_bindings=port_bindings)
        )

        container_id = container.get("Id")
        print 'created container', container_id

        self.client.start(container=container_id)
        print 'started container', container_id

        bindings = {}
        inspect_container = self.client.inspect_container(container=container_id)
        for k,v in inspect_container['NetworkSettings']['Ports'].iteritems():
            if v is None:
                continue
            cport = int(k.split('/')[0])
            bindings[cport] = int(v[0]['HostPort'])

        return (container_id, bindings)

    def delete_container(self, container):
        self.client.stop(container, timeout=0) 
        print 'stopped container', container

        self.client.remove_container(container)
        print 'removed container', container

    def container_ids(self):
        container_ids = []
        containers = self.client.containers()
        for c in containers:
            container_ids.append(c['Id'])

        return container_ids

