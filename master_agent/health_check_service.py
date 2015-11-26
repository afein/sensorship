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
        print "timer is set"
        self.timer = Thread(target=self.poll_health_status)
        self.timer.daemon = True
        print "starting thread"
        self.timer.start()
        print "thread started"

    def poll_health_status(self):
        while True:
            print "polling"
            nodes = self.cluster_state.get_nodes()
            for node in nodes:
                node_ip = nodes[node]["ip"]
                health_check_url = "http://%s:5000/healthz" % node_ip
                resp = requests.get(health_check_url, timeout=6)
                print "healthz"
                print resp
                if resp.status_code != 200:
                    nodes[node]["state"] = "down"
                else:
                    nodes[node]["state"] = "up"
                    data = json.loads(resp.text)
                    containers = self.cluster_state.get_deployed_containers_by_node_id(node)
                    for container_id in data:
                        if container_id in containers:
                            containers[container_id]["state"] = "up"
                            containers[container_id]["cpu_percent"] = data[container_id]["cpu_percent"]
                            containers[container_id]["mem_percent"] = data[container_id]["mem_percent"]
                        else:
                            containers[container_id]["state"] = "down"

                        if node not in self.info_for_node and not self.info_for_node[node]:
                            info_check_url = "http://%s:5000/info" % node_ip
                            resp = requests.get(info_check_url, timeout=6)
                            print "info"
                            print resp
                            if resp.status_code != 200:
                                self.info_for_node[node] = False
                            else:
                                data = json.loads(resp.text)
                                try:
                                    nodes[node]["kernel_version"] = data["kernel_version"]
                                    nodes[node]["num_cores"] = data["num_cores"]
                                    nodes[node]["memory_capacity"] = data["memory_capacity"]
                                    nodes[node]["cpu_frequency_khz"] = data["cpu_frequency_khz"]
                                    self.info_for_node[node] = True
                                except KeyError:
                                    self.info_for_node[node] = False
            print "sleeping"
            sleep(self.interval)
            print "slept"
