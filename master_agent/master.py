from scheduler import Scheduler
from cluster_state import ClusterState
from health_check_service import HealthCheckService
from node_dispatcher import NodeDispatcher
from rest import app as RestService

scheduler = Scheduler(ClusterState(), NodeDispatcher(), "greedy")
RestService.run()
