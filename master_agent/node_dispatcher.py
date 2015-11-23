import requests
import json

class NodeDispatcher(object):
    def __init__(self, port):
        self.agent_listen_port = port 

    def establish_datapipe(self, dst_host, node_host, port, sensor, interval):
        req_payload = json.dumps({'host' : dst_host, 'port' : port, 'sensor' : sensor, 'interval' : interval})
        addr = 'http://%s:%d/datapipe' % (node_host, self.agent_listen_port)
        r = requests.post(addr, data=req_payload)
        return r.status_code

    def destroy_datapipe(self, node_host, dst_host, port, sensor):
        req_payload = json.dumps({'host' : dst_host, 'port' : port, 'sensor' : sensor})
        addr = 'http://%s:%d/datapipe' % (node_host, self.agent_listen_port)
        r = requests.delete(addr, data=req_payload)
        return r.status_code

    def deploy_container(self, host, image, container_ports):
        req_payload = json.dumps({'image' : image, 'ports' : container_ports})
        addr = 'http://%s:%d/container' % (host, self.agent_listen_port)
        r = requests.post(addr, data=req_payload)
        if r.status_code != 200:
            return (None, None)

        resp_payload = json.loads(r.text)
        container_id = resp_payload['container_id']
        port_bindings = resp_payload['port_bindings']
        return (container_id, port_bindings)


    def stop_container(self, host, ID):
        req_payload = json.dumps({'container_id' : ID})
        addr = 'http://%s:%d/container' % (host, self.agent_listen_port)
        r = requests.delete(addr, data=req_payload)
        return r.status_code
