import unittest
from scheduler import Scheduler
from cluster_state import ClusterState
from node_dispatcher import NodeDispatcher

class SchedulerTestcase(unittest.TestCase):
    def setUp(self):
        self.cluster_state = ClusterState()
        self.node_dispatcher = NodeDispatcher()
        self.scheduler = Scheduler(self.cluster_state, self.node_dispatcher)
        self.scheduler.set_policy(self.scheduler.greedy)

    def test_schedule_simple_topology(self):
        self.cluster_state.add_node('Node1', {'name': 'Node1', 'ip': '10.0.0.2', 'mappings': [('Temperature', 'D4')], 'state': 'up'})                       
        self.cluster_state.add_node('Node2', {'name': 'Node2', 'ip': '10.0.0.3', 'mappings': [('Humidity', 'D4')], 'state': 'up'})
        user_config = {'image': 'afein/ubuntussh', 'mapping' : [{'node': 'Node1', 'sensor': 'Temperature', 'port': '4000', 'interval': 500}]}
        node, datapipes = self.scheduler.policy(user_config)
        self.assertEqual(node, 'Node1')
        self.assertItemsEqual(datapipes, {})

    def test_schedule_complex_topology(self):
        self.cluster_state.add_node('Node1', {'name': 'Node1', 'ip': '10.0.0.2', 'mappings': [('Temperature', 'D4'), ('Humidity', 'D5')], 'state': 'up'}) 
        self.cluster_state.add_node('Node2', {'name': 'Node2', 'ip': '10.0.0.3', 'mappings': [('Humidity', 'D4')], 'state': 'up'})
        self.cluster_state.add_node('Node3', {'name': 'Node3', 'ip': '10.0.0.4', 'mappings': [('Temperature', 'D6')], 'state': 'up'}) 
        self.cluster_state.add_node('Node4', {'name': 'Node4', 'ip': '10.0.0.5', 'mappings': [('Light', 'D3')], 'state': 'up'})
        task = {'image': 'afein/ubuntussh', 'mapping': [{'node': 'Node1', 'sensor': 'Temperature', 'port': '4000', 'interval': 100},
                                                               {'node': 'Node2', 'sensor': 'Humidity', 'port': '4001', 'interval': 500},
                                                               {'node': 'Node3', 'sensor': 'Temperature', 'port': '4002', 'interval': 250}]}
        node, datapipes = self.scheduler.policy(task)
        self.assertEqual(node, 'Node1')
        self.assertItemsEqual(datapipes, [{'remote_node': 'Node2', 'sensor': 'Humidity', 'interval': 500},
                                     {'remote_node': 'Node3', 'sensor': 'Temperature', 'interval': 250}])



    def tearDown(self):
        self.scheduler = None

if __name__ == '__main__':
    unittest.main()
