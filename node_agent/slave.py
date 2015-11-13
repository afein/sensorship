import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from sdf import SensorDataFormatter
from vnm import VirtualNetworkManager
from docker_interface import DockerInterface
from rest import RestService

docker = DockerInterface()
sdf = SensorDataFormatter()
vnm = VirtualNetworkManager(sdf)

rest = RestService(docker, vnm)
rest.run()
