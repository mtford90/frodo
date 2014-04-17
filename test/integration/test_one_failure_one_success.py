import unittest
import os
from frodo import Frodo


SCRIPT_DIR = os.path.realpath(__file__)


class TestOneFailureOneSuccess(unittest.TestCase):

    def test_something(self):
        frodo = Frodo('test_one_failure_one_success.yaml')
        frodo.start()
        pass