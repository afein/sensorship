from flask import Flask, render_template, request
from scheduler import Scheduler
import json
from cluster_state import ClusterState

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
    if "state" not in task:
        task["state"] = "off"
    cluster.add_task(task)
    return "OK"

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks_dict = cluster.get_tasks()
    tasks = []
    for key, val in tasks_dict.iteritems():
        new_task = val
        val["id"] = key
        tasks.append(val)
    return json.dumps(tasks)

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

@app.route("/register", methods=["POST"])
def register_node():
    resp = {"something": "implemented"}
    return json.dumps(resp)

if __name__ == "__main__":
        app.run()
