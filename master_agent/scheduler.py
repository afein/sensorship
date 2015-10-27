from threading import Lock

class Scheduler(object):
    def __init__(self, cluster_state, node_dispatcher, policy):
        self.cluster_state = cluster_state
        self.node_dispatcher = node_dispatcher
        self.policy = policy
        self.lock = Lock()

    def schedule(self, user_config):
        with self.lock:
            state = user_config['on']

            if state != 'on':
                raise Exception('Error schedule: task submitted in not in "On" state')

            node = self.policy(user_config)
            # TODO: call dispatcher to deploy container
            # upon successful deployment update cluster state

    def greedy(self, user_config):
        image = user_config['image']
        mappings = user_config['mapping']

        required_sensors = {}
        for mapping in mappings:
            node = mapping['node']
            if node not in required_sensors:
                required_sensors[node] = [mapping['sensor']]
            else:
                required_sensors[node].append(mapping['sensor'])
        
        node_datapipe_mapping = cluster_state.get_node_datapipe_mapping()
        required_datapipes = {}
        for current_node in required_sensors:
            count = 0
            for other_node in required_sensors:
                if other_node != current_node:
                    for sensor in required_sensors[other_node]:
                        if sensor not in node_datapipe_mapping[current_node][other_node]:
                            count += 1
            required_datapipes[current_node] = count
        return min(required_datapipes, key=required_datapipes.get)
