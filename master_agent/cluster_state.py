from threading import Lock
class ClusterState(object):
    ''' Cluster State Singleton '''
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ClusterState, cls).__new__(
                cls, *args, **kwargs)
            cls._instance.new = True
        return cls._instance

    def __init__(self):
        if not self.new:
            return 

        self.nodes = {}
        self.deployed_containers = {}
        self.established_datapipes = {}
        self.established_datapipes_counter = 0
        self.node_datapipe_mapping = {}
        self.available_sensors = {}
        self.available_sensors_counter = 0
        self.tasks = {}
        self.tasks_counter = 0
        self.lock = Lock()

        self.new = False

    def get_nodes(self):
        with self.lock:
            return self.nodes

    def get_node_by_key(self, node_name):
        with self.lock:
            try:
                return self.nodes[node_name]
            except KeyError:
                return None

    def add_node(self, name, node):
        with self.lock:
            self.nodes[name] = node

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

    def add_deployed_containers(self, node_id, container_id):
        with self.lock:
            if node_id not in self.deployed_containers: 
                self.deployed_containers[node_id] = [container_id]
            else:
                self.deployed_containers[node_id].append(container_id)

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
            self.established_datapipes[self.established_datapipes_counter] = datapipe
            self.established_datapipes_counter += 1
            local_node = datapipe.get_local_node()
            remote_node = datapipe.get_remote_node()
            sensor = datapipe.get_sensor()
            if local_node in self.node_datapipe_mapping:
                if remote_node not in self.node_datapipe_mapping[local_node]:
                    self.node_datapipe_mapping[local_node][remote_node] = [sensor]
                else:
                    self.node_datapipe_mapping[local_node][remote_node].append(sensor)
            else:
                self.node_datapipe_mapping[local_node] = {}
                self.node_datapipe_mapping[local_node][remote_node] = [sensor]

    def get_node_datapipe_mapping(self):
        with self.lock:
            return self.node_datapipe_mapping

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
