from flask import Flask, Response, request 
from sdf import SensorDataFormatter
from vnm import VirtualNetworkManager
from docker_interface import DockerInterface

import json
import socket

app = Flask("node-agent")
docker = DockerInterface()
sdf = SensorDataFormatter()
vnm = VirtualNetworkManager(sdf)

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

@app.route("/healthz", methods=["GET"])
def healthz():
    resp = {"healthz": "get"}
    return json.dumps(resp)

@app.route("/datapipe", methods=["POST", "DELETE"])
def datapipe():
    req_json = request.get_json(force=True)
    host = req_json['host']
    port = req_json['port']
    sensor = req_json['sensor']

    if request.method == "POST":
        interval = req_json['interval']
        vnm.create_datapipe(False, host, port, sensor, interval) 
    elif request.method == "DELETE":
        vnm.delete_datapipe(False, host, port, sensor)

    return 'OK'

@app.route("/remote_datapipe", methods=["POST", "DELETE"])
def remote_datapipe():
    return 'OK'

# TODO: container needs setup time
@app.route("/container", methods=["POST", "DELETE"])
def container():
    req_json = request.get_json(force=True)
    image = req_json['image']

    resp = None
    if request.method == "POST":
        ports = req_json['ports'] 
        try:
            (container_id, port_bindings) = docker.run_container(image, ports)
        except Exception as e:
            print e
            raise e
        resp_json = json.dumps({'container_id' : container_id, 'port_bindings' : port_bindings})
        resp = Response(resp_json, status=200, mimetype='application/json') 

    elif request.method == "DELETE":
        try:
            docker.delete_container(image)
        except Exception as e:
            print e
            raise e 
        resp = "OK"

    return resp

@app.route("/sensor_data", methods=["POST"])
def sensor_data():
    req_json = request.get_json(force=True)
    ports = req_json['ports']
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(('192.168.99.100', port)) # TODO: make this work on Linux
            s.send(json.dumps(req_json)) # TODO: data format
        except Exception as e:
            print e
            raise e
        finally:
            s.close()
        
    return "OK"

if __name__ == "__main__":
        app.run()
