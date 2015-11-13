from flask import Flask, Response, request 
import json
import socket

from sensor import *

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

class RestService(object):
    
    def __init__(self, docker, vnm):
        self.app = Flask("node-agent")
        self.docker = docker
        self.vnm = vnm

        @self.app.route("/healthz", methods=["GET"])
        def healthz():
            resp = {"healthz": "get"}
            return json.dumps(resp)

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
            req_json = request.get_json(force=True)
            host = req_json['host']
            port = req_json['port']
            sensor_json = req_json['sensor']
            sensor = Sensor(sensor_json['device'], sensor_json['port'])

            if request.method == "POST":
                interval = req_json['interval']
                self.vnm.create_datapipe(False, host, port, sensor, interval) 
            elif request.method == "DELETE":
                self.vnm.delete_datapipe(False, host, port, sensor)

            return 'OK'
        
        '''
        Do nothing, datapipe receiver implemented as /sensor_data REST endpoint
        '''
        @self.app.route("/remote_datapipe", methods=["POST", "DELETE"])
        def remote_datapipe():
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
            # TODO: container app needs setup time?
            req_json = request.get_json(force=True)

            resp = None
            if request.method == "POST":
                image = req_json['image']
                ports = req_json['ports'] 
                try:
                    (container_id, port_bindings) = self.docker.run_container(image, ports)
                except Exception as e:
                    print '/container POST', e
                    raise e
                resp_json = json.dumps({'container_id' : container_id, 'port_bindings' : port_bindings})
                resp = Response(resp_json, status=200, mimetype='application/json') 

            elif request.method == "DELETE":
                container_id = req_json['container_id']
                try:
                    self.docker.delete_container(container_id)
                except Exception as e:
                    print '/container DELETE', e
                    raise e 
                resp = "OK"

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
                except Exception as e:
                    print '/sensor_data', e
                    raise e
                finally:
                    s.close()
             
            return "OK"

    def run(self):
        self.app.run(host='0.0.0.0', port=5000)
