import os
import socket
from flask import Flask, render_template, request, abort
from flask.json import jsonify
from json import dumps
from requests import get

from cluster_state import ClusterState
from dev.grovepi import grovepi


app = Flask("master-agent", static_folder="./ui/static", template_folder="./ui/templates")

cluster = ClusterState()

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.errorhandler(500)
def internal_error(error):
    return error

app.errorhandler(400)
def custom400(error):
    response = jsonify({'message': error.description})

@app.route("/submit", methods=["POST"])
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
        abort(400, "The image field cannot be blank")

    print "before"
    reponame = task["image"].split("/")
    if len(reponame) != 2:
        abort(400, "Malformed Docker image name or tag")

    repo, name = reponame
    if ":" not in name:
        tag = "latest"
    else:
        nametag =  name.split(":")
        if len(nametag) != 2:
            abort(400, "Malformed Docker tag")
        name, tag = nametag
    print "after"

    resp = get("https://registry.hub.docker.com/v1/repositories/" + repo + "/" + name + "/tags/" + tag)
    if resp.status_code != 200:
        abort(400, "Image does not exist in Docker Hub: " + task["image"])
        return

    if "mappings" not in task or task["mappings"] == "":
        abort(400, "The mappings field cannot be blank")
        return "The image field cannot be blank"

    tokens = task["mappings"].split(",")
    for token in tokens:
        # Tokenization and parsing
        devicesensor = token.strip().split("/")
        if len(devicesensor) != 2:
            abort(400, "Syntax Error while parsing mappings")
        nodename, sensor = devicesensor
        sensorport = sensor.split(":")
        if len(sensorport) != 2:
            abort(400, "Syntax Error while parsing mappings")
        sensor, port = sensorport
        portinterval = port.split(" ") 
        if len(portinterval) != 2:
            abort(400, "Syntax Error while parsing mappings")
        port, interval = portinterval

        # Semantic Validation for Device, Sensor, Port and Interval
        try: 
            intport = int(port)
            if intport < 0 or intport > 65535:
                raise ValueError
        except ValueError:
            abort(400, "Cannot use the specified port \'" + port + "\'")
        try:
            intval = int(interval)
            if intval < 20:
                raise ValueError
        except ValueError:
            abort(400, "Cannot use the specified interval \'" + interval + " ms\'")

        # Node Lookup
        node = cluster.get_node_by_key(nodename) 
        if node is None:
            abort(400, "Error: No such Node: " + nodename)

        # Sensor mapping validation
        mappings = [x for x in node["mappings"].split(",")]
        sensor_types = [data[0] for data in mappings.split(":")]
        if sensor not in sensor_types:
            abort(400, "Error: The requested sensor type, \'", + sensor + "\', has not been configured for node \'" + nodename + "\'")

    cluster.add_task(task)

@app.route("/register", methods=["POST"])
def register_node():
    # TODO(afein): node registration validation
    new_node = request.get_json(force=True)

    if "name" not in new_node:
        abort(400, "The \'name\' field cannot be empty")

    if "ip" not in new_node:
        abort(400, "The \'IP\' field cannot be empty")

    try:
        socket.inet_aton(new_node["ip"])
    except socket.error:
        abort(400, "Invalid IP address")


    if "state" not in node:
        node["state"] = "down"
    cluster.add_node(node)
    return "OK"

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks_dict = cluster.get_tasks()
    tasks = []
    for key, val in tasks_dict.iteritems():
        val["id"] = key
        tasks.append(val)
    return dumps(tasks)

@app.route("/nodes", methods=["GET"])
def get_nodes():
    nodes_dict = cluster.get_nodes()
    nodes = []
    for key, val in nodes_dict.iteritems():
        nodes.append(val)
    return dumps(nodes)


@app.route("/on", methods=["POST"])
def start_task():
    id = int(request.get_json(force=True)["id"])
    task = cluster.get_task_by_id(id)
    task["state"] = "on"
    return dumps(task)

@app.route("/off", methods=["POST"])
def stop_task():
    id = int(request.get_json(force=True)["id"])
    task = cluster.get_task_by_id(id)
    task["state"] = "off"
    return dumps(task)
