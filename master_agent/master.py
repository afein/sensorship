# Inject the parent directory to the PYTHONPATH
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from scheduler import Scheduler
from cluster_state import ClusterState
from health_check_service import HealthCheckService
from node_dispatcher import NodeDispatcher
from rest import RestService

cluster = ClusterState()
dispatcher = NodeDispatcher(5000)

scheduler = Scheduler(cluster, dispatcher)

scheduler.set_policy("greedy")
rest = RestService(cluster, scheduler)
rest.run()
