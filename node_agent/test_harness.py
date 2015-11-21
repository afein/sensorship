import requests
import json

from sensor import *

def create_datapipe(node_host, dst_host, port, sensor, interval):
    req_payload = json.dumps({'host' : dst_host, 'port' : port, 'sensor' : {'device' : sensor.device, 'port' : sensor.port}, 'interval' : interval})
    r = requests.post('http://%s:5000/datapipe' % node_host, data=req_payload)
    assert r.status_code == 200, r.status_code

def delete_datapipe(node_host, dst_host, port, sensor):
    req_payload = json.dumps({'host' : dst_host, 'port' : port, 'sensor' : {'device' : sensor.device, 'port' : sensor.port}})
    r = requests.delete('http://%s:5000/datapipe' % node_host, data=req_payload)
    assert r.status_code == 200, r.status_code

def create_container(node_host, image, ports):
    req_payload = json.dumps({'image' : image, 'ports' : ports})
    r = requests.post('http://%s:5000/container' % node_host, data=req_payload)
    assert r.status_code == 200, r.status_code

    resp_payload = json.loads(r.text)
    container_id = resp_payload['container_id']
    port_bindings = resp_payload['port_bindings']

    return (container_id, port_bindings)

def delete_container(node_host, container_id):
    req_payload = json.dumps({'container_id' : container_id})
    r = requests.delete('http://%s:5000/container' % node_host, data=req_payload)
    assert r.status_code == 200, r.status_code

def healthz(node_host):
    r = requests.get('http://%s:5000/healthz' % node_host)
    assert r.status_code == 200, r.status_code

    return json.loads(r.text)

def info(node_host):
    r = requests.get('http://%s:5000/info' % node_host)
    assert r.status_code == 200, r.status_code

    return json.loads(r.text)

def sdf_state(node_host):
    r = requests.get('http://%s:5000/sdf_state' % node_host)
    assert r.status_code == 200, r.status_code

    return r.text

