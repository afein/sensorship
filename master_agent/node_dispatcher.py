import requests
import json

class NodeDispatcher(object):
    def __init__(self, port):
        self.agent_listen_port = port 

    def establish_datapipe(self, node_host, dst_host, port, sensor, interval):
        req_payload = json.dumps({'host' : dst_host, 'port' : port, 'sensor' : sensor, 'interval' : interval})
        r = requests.post('http://%s:%s/datapipe' % node_host, self.agent_listen_port, data=req_payload)
        return r.status_code

    def destroy_datapipe(self, node_host, dst_host, port, sensor):
        req_payload = json.dumps({'host' : dst_host, 'port' : port, 'sensor' : sensor})
        r = requests.delete('http://%s:%s/datapipe' % node_host, self.agent_listen_port, data=req_payload)
        return r.status_code

    def deploy_container(self, host, image, container_ports):
        print "in deploy container"
        req_payload = json.dumps({'image' : image, 'ports' : container_ports})
        print "After dumps"
        addr = 'http://%s:%d/container' % (host, self.agent_listen_port)
        print addr
        r = requests.post(addr, data=req_payload)
        print "After post"
        if r.status_code != 200:
            return (None, None)

        resp_payload = json.loads(r.text)
        container_id = resp_payload['container_id']
        port_bindings = resp_payload['port_bindings']
        return (container_id, port_bindings)


    def stop_container(self, host, ID):
        req_payload = json.dumps({'image' : image})
        r = requests.delete('http://%s:%s/container' % host, self.agent_listen_port, data=req_payload)
        return r.status_code
