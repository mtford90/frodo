import os
import unittest
from frodo import Frodo


# noinspection PyProtectedMember
class TestFrodo(unittest.TestCase):

    def test_config_path(self):
        path = 'xxx'
        f = Frodo(config_path=path)
        self.assertEqual(f._config_path, path)

    def test_default_config_path(self):
        path = '/path/to/conf'
        os.environ['FRODO_CONF'] = path
        f = Frodo()
        self.assertEqual(f._config_path, path)