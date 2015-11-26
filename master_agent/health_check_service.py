import requests
import json
from threading import Thread
from time import sleep

class HealthCheckService(object):
    def __init__(self, interval, cluster_state):
        self.interval = interval # in seconds
        self.cluster_state = cluster_state
        self.info_for_node = {}
        self.set_timer()

    def set_timer(self):
        self.timer = Thread(target=self.poll_health_status)
        self.timer.daemon = True
        self.timer.start()

    def poll_health_status(self):
        while True:
            nodes = self.cluster_state.get_nodes()
            for node in nodes:
                node_ip = nodes[node]["ip"]
                health_check_url = "http://%s:5000/healthz" % node_ip
                resp = requests.get(health_check_url, timeout=6)
                if resp.status_code != 200:
                    nodes[node]["state"] = "down"
                else:
                    nodes[node]["state"] = "up"
		    nodes[node]["containers"] = []
                    data = json.loads(resp.text)
                    containers = self.cluster_state.get_deployed_containers_by_node_id(node)
		    if containers is not None:
			for container_id in data:
			    if container_id in containers:
				containers[container_id]["state"] = "up"
				containers[container_id]["cpu_percent"] = data[container_id]["cpu_percent"]
				containers[container_id]["mem_percent"] = data[container_id]["mem_percent"]
			    else:
				containers[container_id]["state"] = "down"
			    for container_id in containers:
				nodes[node]["containers"].append({
				    "id" : container_id,
				    "state" : containers[container_id]["state"],
				    "cpu_percent" : containers[container_id]["cpu_percent"],
				    "mem_percent" : containers[container_id]["mem_percent"]
				})

                    if node not in self.info_for_node:
                        info_check_url = "http://%s:5000/info" % node_ip
                        resp = requests.get(info_check_url, timeout=6)
                        if resp.status_code == 200:
                            data = json.loads(resp.text)
                            try:
                                nodes[node]["info"] = {}
                                nodes[node]["info"]["kernel_version"] = data["kernel_version"]
                                nodes[node]["info"]["num_cores"] = data["num_cores"]
                                nodes[node]["info"]["memory_capacity"] = data["memory_capacity"]
                                nodes[node]["info"]["cpu_frequency_khz"] = data["cpu_frequency_khz"]
                                self.info_for_node[node] = True
                            except KeyError:
                                self.info_for_node[node] = False
            sleep(self.interval)
