from flask import Flask, Response, request 
import json
import socket
import sys, traceback

from sensor import *
from util import *

class RestService(object):
    
    def __init__(self, docker, vnm):
        self.app = Flask("node-agent")
        self.docker = docker
        self.vnm = vnm


        '''
        GET: Get health monitoring metrics for running containers

            response contains {container_id : {'cpu_percent' : value, 'mem_percent' : value}, ...}
        '''
        @self.app.route("/healthz", methods=["GET"])
        def healthz():
            resp = None
            try:
                container_ids = self.docker.container_ids()
                metrics_json = json.dumps(cadvisor_metrics(container_ids))
                resp = Response(metrics_json, status=200, mimetype='application/json')
            except:
                traceback.print_exc(file=sys.stderr)
                raise

            return resp

        '''
        POST: Create a datapipe(host, port, sensor, interval)
            host - IP of destination node
            port - host port binded to container
            sensor - device name and attached port
            interval - period for polling (in seconds)

        DELETE: Delete a datapipe(host, port, sensor)
            host - IP of destination node
            port - host port binded to container
            sensor - device name and attached port
        '''
        @self.app.route("/datapipe", methods=["POST", "DELETE"])
        def datapipe():
            try:
                req_json = request.get_json(force=True)
                host = host_cast(req_json['host'])
                port = port_cast(req_json['port'])
                sensor_json = req_json['sensor']
                sensor = Sensor(sensor_json['device'], sensor_json['port'])

                if request.method == "POST":
                    interval = interval_cast(req_json['interval'])
                    self.vnm.create_datapipe(host, port, sensor, interval) 
                elif request.method == "DELETE":
                    self.vnm.delete_datapipe(host, port, sensor)

            except:
                traceback.print_exc(file=sys.stderr)
                raise

            return 'OK'
        
        '''
        POST: Create and start a container(image, ports) 
            image - name of container image
            ports - array of ports used by container
            
            response returns the container_id and port bindings {container_port : host_port}

        DELETE: Delete a container(container_id)
            container_id - string id for container
        '''
        @self.app.route("/container", methods=["POST", "DELETE"])
        def container():
            try:
                req_json = request.get_json(force=True)
                resp = None
                if request.method == "POST":
                    image = str(req_json['image'])
                    ports = req_json['ports'] 
                    port_array = [port_cast(x) for x in ports]
                    (container_id, port_bindings) = self.docker.run_container(image, port_array)

                    resp_json = json.dumps({'container_id' : container_id, 'port_bindings' : port_bindings})
                    resp = Response(resp_json, status=200, mimetype='application/json') 

                elif request.method == "DELETE":
                    container_id = req_json['container_id']
                    self.docker.delete_container(container_id)

                    resp = "OK"

            except e:
                traceback.print_exc(file=sys.stderr)
                raise e

            return resp

        '''
        POST - timeslice of sensor data forwarded to appropriate container ports 
        '''
        @self.app.route("/sensor_data", methods=["POST"])
        def sensor_data():
            req_json = request.get_json(force=True)
            ports = req_json['ports']
            payload = req_json['data']

            for port in ports:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    s.connect(('', port))
                    s.send(payload)
                except:
                    traceback.print_exc(file=sys.stderr)
                finally:
                    s.close()
             
            return "OK"
        
        '''
        GET - state of SDF for debugging
        '''
        @self.app.route("/sdf_state", methods=["GET"])
        def sdf_state():
            sdf_state = self.vnm.sdf.__repr__()
            resp = Response(sdf_state, status=200, mimetype='text/plain')

            return resp

            
    def run(self):
        self.app.run(host='0.0.0.0', port=5000)
