from threading import Lock
class ClusterState(object):
    def __init__(self):
        self.configured_nodes = {}
        self.configured_nodes_counter = 0
        self.deployed_containers = {}
        self.deployed_containerS_counter = 0
        self.established_datapipes = {}
        self.established_datapipes_counter = 0
        self.available_sensors = {}
        self.available_sensors_counter = 0
        self.tasks = {}
        self.tasks_counter = 0
        self.lock = Lock()

    def get_configured_nodes(self):
        with self.lock:
            return self.configured_nodes

    def get_configured_node_by_id(self, node_id):
        with self.lock:
            try:
                return self.configured_nodes[node_id]
            except KeyError:
                return None

    def add_configured_nodes(self, node):
        with self.lock:
            self.configured_nodes[self.configured_nodes_counter] = node
            self.configured_nodes_counter += 1

    def get_tasks(self):
        with self.lock:
            return self.tasks

    def get_task_by_id(self, task_id):
        with self.lock:
            return self.tasks[task_id]

    def add_task(self, task):
        with self.lock:
            self.tasks[self.tasks_counter] = task
            self.tasks_counter += 1

    def get_deployed_containers(self):
        with self.lock:
            return self.deployed_containers

    def get_deployed_containers_by_node_id(self, node_id):
        with self.lock:
            try:
                return self.deployed_containers[node_id]
            except KeyError:
                return None

    def add_deployed_containers(self, node_id):
        with self.lock:
            if node_id not in self.deployed_containers: 
                self.deployed_containers[node_id] = [self.deployed_containers_counter]
            else:
                node_container_mapping = self.deployed_containers[node_id]
                node_container_mapping.append(self.deployed_containers_counter)
            self.deployed_containers_counter += 1

    def get_established_datapipes(self):
        with self.lock:
            return self.established_datapipes

    def get_established_datapipe_by_id(self, datapipe_id):
        with self.lock:
            try:
                return self.established_datapipes[datapipe_id]
            except KeyError:
                return None

    def add_established_datapipes(self, datapipe):
        with self.lock:
            self.established_datapipes[self.configured_datapipes_counter] = datapipe
            self.established_datapipes_counter += 1

    def get_available_sensors(self):
        with self.lock:
            return self.available_sensors

    def get_available_sensor_by_id(self, sensor_id):
        with self.lock:
            try:
                return self.available_sensors[sensor_id]
            except KeyError:
                return None

    def add_available_sensors(self, sensor):
        with self.lock:
            self.available_sensors[self.available_sensors_counter] = sensor
            self.available_sensors_counter += 1
