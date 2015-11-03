import unittest
from scheduler import Scheduler
from cluster_state import ClusterState
from node_dispatcher import NodeDispatcher

class SchedulerTestcase(unittest.TestCase):
    def setUp(self):
        self.cluster_state = ClusterState()
        self.node_dispatcher = NodeDispatcher()
        self.scheduler = Scheduler(cluster_state, node_dispatcher, greedy)

    def test_schedule_simple_topology(self):
        user_config = {'image': 'afein/ubuntussh', 'mappings' : [{'node': 1, 'sensor': 'temperature', 'port': '4000', 'interval': 500}]}
        node, datapipes = self.scheduler.schedule(user_config)
        self.assertEqual(1, 1)

    def tearDown(self):
        self.scheduler.dispose()
        self.scheduler = None
