from flask import Flask, render_template, request, abort
from flask.json import jsonify
from scheduler import Scheduler
import json
from cluster_state import ClusterState
import requests

#TODO: fix relative paths related to the Driver
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

    resp = requests.get("https://registry.hub.docker.com/v1/repositories/" + repo + "/" + name + "/tags/" + tag)
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
        device, sensor = devicesensor
        sensorport = sensor.split(":")
        if len(sensorport) != 2:
            abort(400, "Syntax Error while parsing mappings")
        sensor, port = sensorport
        portinterval = port.split(" ") 
        if len(portinterval) != 2:
            abort(400, "Syntax Error while parsing mappings")
        port, interval = portinterval

        # Semantic Validation for Device, Sensor, Port and Interval
        # TODO(afein): device/sensor semantic validation based on registration
        try: 
            intport = int(port)
            if intport < 0 or intport > 65535:
                raise ValueError
        except ValueError:
            abort(400, "Cannot use the specified port \'" + port + "\'")
        try:
            intval = int(interval)
        except ValueError:
            abort(400, "Cannot use the specified interval \'" + interval + "\'")

    cluster.add_task(task)
    return "OK"

@app.route("/register", methods=["POST"])
def register_node():
    # TODO(afein): node registration validation
    node = request.get_json(force=True)
    if "state" not in node:
        node["state"] = "down"
    cluster.add_configured_nodes(node)
    return "OK"

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks_dict = cluster.get_tasks()
    tasks = []
    for key, val in tasks_dict.iteritems():
        val["id"] = key
        tasks.append(val)
    return json.dumps(tasks)

@app.route("/nodes", methods=["GET"])
def get_nodes():
    nodes_dict = cluster.get_configured_nodes()
    nodes = []
    for key, val in nodes_dict.iteritems():
        val["id"] = key
        nodes.append(val)
    return json.dumps(nodes)


@app.route("/on", methods=["POST"])
def start_task():
    id = int(request.get_json(force=True)["id"])
    print id
    task = cluster.get_task_by_id(id)
    task["state"] = "on"
    print cluster.get_task_by_id(id)
    return json.dumps(task)

@app.route("/off", methods=["POST"])
def stop_task():
    id = int(request.get_json(force=True)["id"])
    print id
    task = cluster.get_task_by_id(id)
    task["state"] = "off"
    print cluster.get_task_by_id(id)
    return json.dumps(task)

if __name__ == "__main__":
        app.run()
