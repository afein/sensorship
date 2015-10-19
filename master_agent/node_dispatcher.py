class NodeDispatcher(object):
    def __init__(self):
        pass

    def establish_datapipe(self, node1, node2, sensor, interval):
        pass

    def destroy_datapipe(self, node1, node2, sensor):
        pass

    def deploy_container(self, host, image, sensor_mappings):
        pass

    def stop_container(self, host, ID):
        pass
