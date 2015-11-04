import os
import socket
from flask import Flask, render_template, request
from werkzeug.exceptions import BadRequest
from flask.json import jsonify
from json import dumps
from requests import get

from dev.grovepi import grovepi

def abort(message):
    resp = BadRequest()
    resp.description=message
    return resp

class RestService(object):
    def __init__(self, cluster, scheduler):
        self.cluster = cluster
        self.app = Flask("master-agent", static_folder="./ui/static", template_folder="./ui/templates")

        @self.app.route("/", methods=["GET"])
        def home():
            return render_template("index.html")

        @self.app.errorhandler(500)
        def internal_error(error):
            return error

        @self.app.errorhandler(400)
        def custom400(error):
            response = jsonify({'message': error.description})

        @self.app.route("/submit", methods=["POST"])
        def submit_task():
            '''
                The /submit endpoint retrieves a task object in JSON format, 
                validates that the task is runnable in the current cluster
                and stores the task in cluster_state.
            '''
            task = request.get_json(force=True)
            if "state" not in task or ("state" != "off" and "state" != "on"):
                task["state"] = "off"

            if "image" not in task or task["image"] == "":
                return abort("The image field cannot be blank")

            reponame = task["image"].split("/")
            if len(reponame) != 2:
                return abort("Malformed Docker image name or tag")

            repo, name = reponame
            if ":" not in name:
                tag = "latest"
            else:
                nametag =  name.split(":")
                if len(nametag) != 2:
                    return abort("Malformed Docker tag")
                name, tag = nametag

            resp = get("https://registry.hub.docker.com/v1/repositories/" + repo + "/" + name + "/tags/" + tag)
            if resp.status_code != 200:
                return abort("Image \'" + task["image"] + "\' does not exist in Docker Hub")

            if "mappings" not in task or task["mappings"] == "":
                return abort("The mappings field cannot be blank")

            tokens = task["mappings"].split(",")
            for token in tokens:
                # Tokenization and parsing
                devicesensor = token.strip().split("/")
                if len(devicesensor) != 2:
                    return abort("Syntax Error while parsing mappings")
                nodename, sensor = devicesensor
                sensorport = sensor.split(":")
                if len(sensorport) != 2:
                    return abort("Syntax Error while parsing mappings")
                sensor, port = sensorport
                portinterval = port.split(" ") 
                if len(portinterval) != 2:
                    return abort("Syntax Error while parsing mappings")
                port, interval = portinterval

                # Semantic Validation for Device, Sensor, Port and Interval
                try: 
                    intport = int(port)
                    if intport < 0 or intport > 65535:
                        raise ValueError
                except ValueError:
                    return abort("Cannot use the specified port \'" + port + "\'")
                try:
                    intval = int(interval)
                    if intval < 20:
                        raise ValueError
                except ValueError:
                    return abort("Cannot use the specified interval \'" + interval + " ms\'")

                # Node Lookup
                node = self.cluster.get_node_by_key(nodename) 
                if node is None:
                    return abort("Error: No such Node: " + nodename)

                # Sensor mapping validation
                sensor_types = []
                for sensor, _ in node["mappings"]:
                    sensor_types.append(sensor)

                if sensor not in sensor_types:
                    return abort("Error: The requested sensor type, \'", + sensor + "\', has not been configured for node \'" + nodename + "\'")

            self.cluster.add_task(task)
            return "OK"

        @self.app.route("/register", methods=["POST"])
        def register_node():
            new_node = request.get_json(force=True)

            if "name" not in new_node:
                abort(400, "The \'name\' field cannot be empty")

            if "ip" not in new_node:
                abort(400, "The \'IP\' field cannot be empty")

            # Check if the IP is syntactically correct
            try:
                socket.inet_aton(new_node["ip"])
            except socket.error:
                abort(400, "Invalid IP address")

            if "mappings" not in new_node:
                abort(400, "The \'mappings\' field cannot be empty")

            tokens = new_node["mappings"].split(",")
            new_mappings = []
            for token in tokens:
                # Tokenization and parsing
                sensorpin = token.strip().split(":")
                if len(sensorpin) != 2:
                    abort(400, "Syntax Error while parsing mappings")

                sensor, pin = sensorpin

                #TODO: lookup sensor type(analog/digital) or fail
                connection = "digital"

                if connection not in grovepi :
                    abort(400, "The requested pin is not available for this sensor type")

                if pin not in grovepi[connection]:
                    abort(400, "The requested pin is not available for this sensor type")
                new_mappings.append((sensor, pin))
                
            if "state" not in new_node:
                new_node["state"] = "down"
            new_node["mappings"] = new_mappings
            self.cluster.add_node(new_node["name"], new_node)
            return "OK"

        @self.app.route("/tasks", methods=["GET"])
        def get_tasks():
            tasks_dict = self.cluster.get_tasks()
            tasks = []
            for key, val in tasks_dict.iteritems():
                val["id"] = key
                tasks.append(val)
            return dumps(tasks)

        @self.app.route("/nodes", methods=["GET"])
        def get_nodes():
            nodes_dict = self.cluster.get_nodes()
            nodes = []
            for key, val in nodes_dict.iteritems():
                nodes.append(val)
            return dumps(nodes)


        @self.app.route("/on", methods=["POST"])
        def start_task():
            id = int(request.get_json(force=True)["id"])
            task = self.cluster.get_task_by_id(id)
            task["state"] = "on"
            return dumps(task)

        @self.app.route("/off", methods=["POST"])
        def stop_task():
            id = int(request.get_json(force=True)["id"])
            task = self.cluster.get_task_by_id(id)
            task["state"] = "off"
            return dumps(task)

    def run(self):
        self.app.run()
