from threading import Lock

class Scheduler(object):
    def __init__(self, cluster_state, node_dispatcher):
        self.cluster_state = cluster_state
        self.node_dispatcher = node_dispatcher
        self.policy = None
        self.lock = Lock()
    
    def set_policy(self, policy):
        with self.lock:
            self.policy = policy

    def schedule(self, task):
        with self.lock:
            state = task['on']

            if state != 'on':
                raise Exception('Error schedule: task submitted in not in "On" state')

            node, datapipes = self.policy(task)
            container_id, port_bindings = node_dispatcher.deploy_container(task)
            mappings = task['mappings']
            if port_bindings != None:
                for datapipe in datapipes:
                    port = None
                    for mapping in task['mappings']:
                        for p in port_bindings:
                            if p == mapping['port']:
                                port = port_bindings[p]
                                break
                    status_code = node_dispatcher.establish_datapipe(node, datapipe['remote_node'], port, datapipe['sensor'], datapipe['interval'])
                    if status_code != 200:
                        raise Exception('Error when establishing datapipe')
                cluster_state.add_deployed_containers(node)

    def greedy(self, task):
        image = task['image']
        mappings = task['mappings']

        required_sensors = {}
        for mapping in mappings:
            node = mapping['node']
            if node not in required_sensors:
                required_sensors[node] = [{'sensor': mapping['sensor'], 'interval': mapping['interval']}]
            else:
                required_sensors[node].append({'sensor': mapping['sensor'], 'interval': mapping['interval']})
        node_datapipe_mapping = self.cluster_state.get_node_datapipe_mapping()
        required_datapipes = {}
        actual_datapipes = {}
        for current_node in required_sensors:
            count = 0
            for other_node in required_sensors:
                if other_node != current_node:
                    for sensor in required_sensors[other_node]:
                        if current_node in node_datapipe_mapping and other_node in node_datapipe_mapping[current_node]:
                            if sensor['sensor'] not in node_datapipe_mapping[current_node][other_node]:
                                count += 1
                                if current_node not in actual_datapipes:
                                    actual_datapipes[current_node] = [{'remote_node': other_node, 'sensor': sensor['sensor'], 'interval': sensor['interval']}]
                                else:
                                    actual_datapipes[current_node].append({'remote_node': other_node, 'sensor': sensor['sensor'], 'interval': sensor['interval']})
                        else:
                            count += 1
                            if current_node not in actual_datapipes:
                                actual_datapipes[current_node] = [{"remote_node": other_node, 'sensor': sensor['sensor'], 'interval': sensor['interval']}]
                            else:
                                actual_datapipes[current_node].append({"remote_node": other_node, 'sensor': sensor['sensor'], 'interval': sensor['interval']})
            required_datapipes[current_node] = count
        scheduled_node = min(required_datapipes, key=required_datapipes.get)
        if actual_datapipes == {}:
            scheduled_datapipes = {}
        else:
            scheduled_datapipes = actual_datapipes[scheduled_node]
        return (scheduled_node, scheduled_datapipes)
