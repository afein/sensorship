from threading import Lock
from lib.datapipe import Datapipe

class Scheduler(object):
    def __init__(self, cluster_state, node_dispatcher):
        self.cluster_state = cluster_state
        self.node_dispatcher = node_dispatcher
        self.policy = None
        self.lock = Lock()
    
    def set_policy(self, policy):
        with self.lock:
            if policy == "greedy":
                self.policy = self.greedy
            else:
                raise Exception("invalid policy")

    def schedule(self, task):
        with self.lock:
            if task['state'] != 'on':
                raise Exception('Error schedule: task submitted in not in "On" state')

            mappings = task['mappings']
            container_ports = [int(x["port"]) for x in mappings]

            node, datapipes = self.policy(task)

            print "node: "
            print node
            print "datapipes: "
            print datapipes
            node_object = self.cluster_state.get_node_by_key(node)
            ip_addr = node_object["ip"]
            container_id, port_bindings = self.node_dispatcher.deploy_container(ip_addr, task["image"], container_ports)
            if port_bindings is None:
                return #TODO error

            print "container_id + port_bindings: "
            print container_id
            print port_bindings


            for datapipe in datapipes:
                port = None
                sensor = {}
                for mapping in mappings:
                    if datapipe["sensor"] == mapping["sensor"]:
                        for p in port_bindings:
                            if p == mapping["port"]:
                                port = port_bindings[p]
                                sensor["device"] = mapping["sensor"]
                                sensor["port"] = mapping["port"]
                                break
                status_code = node_dispatcher.establish_datapipe(node, datapipe["remote_node"], port, sensor, datapipe["interval"])
                if status_code != 200:
                    raise Exception('Error when establishing datapipe')
                self.cluster_state.add_established_datapipes(Datapipe(datapipe["sensor"], node, datapipe["remote_node"]))

            self.cluster_state.add_deployed_containers(node, container_id)
            print "deployed_containers: "
            print self.cluster_state.get_deployed_containers()

    def greedy(self, task):
        required_sensors = {}
        for mapping in task['mappings']:
            node = mapping['node']
            new_sensor = {'sensor': mapping['sensor'],
                          'interval': mapping['interval']
            }
            if node not in required_sensors:
                required_sensors[node] = [new_sensor]
            else:
                required_sensors[node].append(new_sensor)

        node_datapipe_mapping = self.cluster_state.get_node_datapipe_mapping()
        required_datapipes = {}
        actual_datapipes  = {}
        print "first for loop"

        for current_node in required_sensors:
            count = 0
            print "second for loop"
            for other_node in required_sensors:
                print "third for loop"
                for sensor in required_sensors[other_node]:
                    if current_node in node_datapipe_mapping and other_node in node_datapipe_mapping[current_node] and sensor["sensor"] in node_datapipe_mapping[current_node][other_node]:
                        continue

                    #Establish new datapipe
                    print "establishing new datapipe"
                    count += 1
                    new_datapipe = {'remote_node': other_node, 
                                    'sensor': sensor['sensor'], 
                                    'interval': sensor['interval']
                    }
                    if current_node not in actual_datapipes:
                        actual_datapipes[current_node] = [new_datapipe]
                    else:
                        actual_datapipes[current_node].append(new_datapipe)
            required_datapipes[current_node] = count
        scheduled_node = min(required_datapipes, key=required_datapipes.get)
        print "scheduled node"
        print scheduled_node
        scheduled_datapipes = actual_datapipes[scheduled_node]
        return (scheduled_node, scheduled_datapipes)
