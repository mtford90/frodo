import unittest
import os
from frodo import Frodo


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


class TestOneFailureOneSuccess(unittest.TestCase):

    def test_something(self):
        frodo = Frodo(SCRIPT_DIR+'/test_one_failure_one_success.yaml')
        frodo.start()
        frodo_tests = frodo.configuration.tests
        self.assertEqual(len(frodo_tests), 1)
        self.assertIn('mytest', frodo_tests)
        frodo_test = frodo_tests['mytest']
        self.assertEqual(len(frodo_test.tests), 2)
