class ClusterState(object):
    def __init__(self):
        self.configured_nodes = {}
        self.deployed_containers = {}
        self.established_datapipes = {}
        self.available_sensors = {}

    def get_configured_nodes(self):
        return self.configured_nodes

    def set_configured_nodes(self, node):
        self.configured_nodes[node.get_id()] = node

    def get_deployed_containers(self):
        return self.deployed_containers

    def set_deployed_containers(self, nodeID, containerID):
        try:
            node_container_mapping = self.deployed_containers[nodeID]
            node_container_mapping.append(containerID)
        except KeyError:
            self.deployed_containers[nodeID] = [containerID]

    def get_established_datapipes(self):
        return self.established_datapipes

    def set_established_datapipes(self, datapipe):
        self.established_datapipes[datapipe.get_id()] = datapipe

    def get_available_sensors(self):
        return self.available_sensors

    def set_available_sensors(self, sensor):
        self.available_sensors[sensor.get_id()] = sensor
