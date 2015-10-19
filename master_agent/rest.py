from flask import Flask
from scheduler import Scheduler
import json

app = Flask("master-agent")

@app.route("/submit", methods=["POST"])
def submit_job():
    resp = {"something": "implemented"}
    return json.dumps(resp)

@app.route("/on", methods=["POST"])
def start_job():
    resp = {"something": "implemented"}
    return json.dumps(resp)

@app.route("/off", methods=["POST"])
def stop_job():
    resp = {"something": "implemented"}
    return json.dumps(resp)

@app.route("/register", methods=["POST"])
def register_node():
    resp = {"something": "implemented"}
    return json.dumps(resp)

if __name__ == "__main__":
        app.run()
