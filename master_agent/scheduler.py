from threading import Lock

class Scheduler(object):
    def __init__(self, cluster_state, node_dispatcher, policy):
        self.cluster_state = cluster_state
        self.node_dispatcher = node_dispatcher
        self.policy = policy
        self.lock = Lock()

    def schedule(self, task):
        with self.lock:
            state = task['on']

            if state != 'on':
                raise Exception('Error schedule: task submitted in not in "On" state')

            node, datapipes = self.policy(task)
            if node_dispatcher.deploy_container(task):
                for datapipe in datapipes:
                    flag = node_dispatcher.establish_datapipe(node, datapipe['remote_node'], datapipe['sensor'], datapipe['interval'])
                    if not flag:
                        raise Exception('Error when establishing datapipe')
                cluster_state.add_deployed_containers(node)

    def greedy(self, task):
        image = task['image']
        mappings = task['mapping']

        required_sensors = {}
        for mapping in mappings:
            node = mapping['node']
            if node not in required_sensors:
                required_sensors[node] = [{'sensor': mapping['sensor'], 'interval': mapping['interval']}]
            else:
                required_sensors[node].append({'sensor': mapping['sensor'], 'interval': mapping['interval']})
        
        node_datapipe_mapping = cluster_state.get_node_datapipe_mapping()
        required_datapipes = {}
        actual_datapipes = {}
        for current_node in required_sensors:
            count = 0
            for other_node in required_sensors:
                if other_node != current_node:
                    for sensor in required_sensors[other_node]:
                        if sensor['sensor'] not in node_datapipe_mapping[current_node][other_node]:
                            count += 1
                            actual_datapipes[current_node] = {'remote_node': other_node, 'sensor': sensor['sensor'], 'interval': sensor['interval']}
            required_datapipes[current_node] = count
        scheduled_node = min(required_datapipes, key=required_datapipes.get)
        scheduled_datapipes = actual_datapipes[scheduled_node]
        return (scheduled_node, scheduled_datapipes)
