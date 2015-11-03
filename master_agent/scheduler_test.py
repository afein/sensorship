import unittest
from scheduler import Scheduler

class SchedulerTestcase(unittest.TestCase):
    def setUp(self):
        self.scheduler = Scheduler()

    def test_schedule_X(self):
        self.assertEqual(1, 1)

    def tearDown(self):
        pass
