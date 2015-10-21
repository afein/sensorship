from flask import Flask, render_template, request
from scheduler import Scheduler
import json

app = Flask("master-agent", static_folder="./ui/static", template_folder="./ui/templates")

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.errorhandler(500)
def internal_error(error):
    return error

@app.route("/submit", methods=["POST"])
def submit_task():
    return json.dumps(request.get_json(force=True))

@app.route("/tasks", methods=["GET"])
def get_tasks():
    task = {"id": 1, 
            "image":"afein/container:latest",
            "mappings": "board/sensor:89000",
            "state": "off"
    }
    return json.dumps([task])

@app.route("/on", methods=["POST"])
def start_task():
    resp = {"something": "implemented"}
    return json.dumps(resp)

@app.route("/off", methods=["POST"])
def stop_task():
    resp = {"something": "implemented"}
    return json.dumps(resp)

@app.route("/register", methods=["POST"])
def register_node():
    resp = {"something": "implemented"}
    return json.dumps(resp)

if __name__ == "__main__":
        app.run()
