import requests
import json
import time

class HealthCheckService(object):
    def __init__(self, interval, cluster_state):
        self.interval = interval # in milliseconds
        self.cluster_state = cluster_state

    def get_interval(self):
        return self.interval

    def set_interval(self, interval):
        self.interval = interval

    def poll_health_status(self):
        nodes = self.cluster_state.get_configured_nodes()
        while True:
            for node_id in nodes:
                health_check_url = "http://" + nodes[node_id].get_ip() + "/healthz"
                resp = requests.get(health_check_url)
                if resp.status_code != 200:
                    nodes[node_id].set_healthy = False
                else:
                    nodes[node_id].set_healthy = True
                    data = json.dumps(resp.content)
                    nodes[node_id].set_cpu(data["cpu"])
                    nodes[node_id].set_memory(data["memory"])
            time.sleep(float(self.get_interval() / 1000)) # time.sleep expects the duration in seconds
