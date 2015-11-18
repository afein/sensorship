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
        nodes = self.cluster_state.get_nodes()
        while True:
            for node in nodes:
                health_check_url = "http://%s/healthz" % nodes[node]["ip"]
                resp = requests.get(health_check_url)
                if resp.status_code != 200:
                    nodes[node]["state"] = "down"
                else:
                    nodes[node]["state"] = "up"
                    #TODO add monitoring data to cluster_state 
                    #data = json.loads(resp.text)
            time.sleep(float(self.get_interval() / 1000)) # time.sleep expects the duration in seconds
