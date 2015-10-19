from flask import Flask, request
from virtual_network_manager import VirtualNetworkManager
import json

app = Flask("node-agent")

@app.route("/healthz", methods=["GET"])
def healthz():
    resp = {"healthz": "get"}
    return json.dumps(resp)

@app.route("/datapipe", methods=["POST", "DELETE"])
def datapipe():
    if request.method == "POST":
        resp = {"datapipe": "post"}
    elif request.method == "DELETE":
        resp = {"datapipe": "delete"}
    return json.dumps(resp)

@app.route("/remote_datapipe", methods=["POST", "DELETE"])
def remote_datapipe():
    if request.method == "POST":
        resp = {"remote_datapipe": "POST"}
    elif request.method == "DELETE":
        resp = {"remote_datapipe": "DELETE"}
    return json.dumps(resp)

@app.route("/container", methods=["POST", "DELETE"])
def container():
    if request.method == "POST":
        resp = {"container": "POST"}
    elif request.method == "DELETE":
        resp = {"container": "DELETE"}
    return json.dumps(resp)


if __name__ == "__main__":
        app.run()
