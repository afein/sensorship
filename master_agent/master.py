from scheduler import Scheduler
from cluster_state import ClusterState
from health_check_service import HealthCheckService
from node_dispatcher import NodeDispatcher

# Add the parent directory to the PYTHONPATH
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

# Import and configure the REST service
from rest import app as RestService

scheduler = Scheduler(ClusterState(), NodeDispatcher(), "greedy")
RestService.run()
