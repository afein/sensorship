# Inject the parent directory to the PYTHONPATH
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from scheduler import Scheduler
from cluster_state import ClusterState
from health_check_service import HealthCheckService
from node_dispatcher import NodeDispatcher

# Add the parent directory to the PYTHONPATH
from rest import RestService

# Import and configure the REST service

cluster = ClusterState()
scheduler = Scheduler(cluster, NodeDispatcher(), "greedy")
rest = RestService(cluster, scheduler)
rest.run()

