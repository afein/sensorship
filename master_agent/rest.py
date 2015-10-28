from flask import Flask, render_template, request, abort
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

@app.route("/submit", methods=["POST"])
def submit_task():
    task = request.get_json(force=True)
    if "state" not in task or ("state" != "off" and "state" != "on"):
        task["state"] = "off"

    if "image" not in task or task["image"] == "":
        abort(402)

    repo, name = task["image"].split("/")
    if ":" not in name:
        tag = "latest"
    else:
        name, tag = name.split(":")

    resp = requests.get("https://registry.hub.docker.com/v1/repositories/" + repo + "/" + name + "/tags/" + tag)
    if resp.status_code != 200:
        abort(401)
        return "Image does not exist in Docker Hub: " + task["image"]

    if "mappings" not in task:
        abort(402)

# TODO(afein): validate node/sensor:port-iv mappings

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
