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

    def get_configured_nodes(self):
        return self.configured_nodes

    def get_configured_node_by_id(self, node_id):
        try:
            return self.configured_nodes[node_id]
        except KeyError:
            return None

    def add_configured_nodes(self, node):
        self.configured_nodes[self.configured_nodes_counter] = node
        self.configured_nodes_counter += 1

    def get_deployed_containers(self):
        return self.deployed_containers

    def get_deployed_containers_by_node_id(self, node_id):
        try:
            return self.deployed_containers[node_id]
        except KeyError:
            return None

    def add_deployed_containers(self, node_id):
        try:
            node_container_mapping = self.deployed_containers[node_id]
            node_container_mapping.append(self.deployed_containers_counter)
        except KeyError:
            self.deployed_containers[node_id] = [self.deployed_containers_counter]
        self.deployed_containers_counter += 1

    def get_established_datapipes(self):
        return self.established_datapipes

    def get_established_datapipe_by_id(self, datapipe_id):
        try:
            return self.established_datapipes[datapipe_id]
        except KeyError:
            return None

    def add_established_datapipes(self, datapipe):
        self.established_datapipes[self.configured_datapipes_counter] = datapipe
        self.established_datapipes_counter += 1

    def get_available_sensors(self):
        return self.available_sensors

    def get_available_sensor_by_id(self, sensor_id):
        try:
            return self.available_sensors[sensor_id]
        except KeyError:
            return None

    def add_available_sensors(self, sensor):
        self.available_sensors[self.available_sensors_counter] = sensor
        self.available_sensors_counter += 1
