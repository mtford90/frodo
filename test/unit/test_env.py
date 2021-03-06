import unittest

from mock import NonCallableMock

from runner.frodo_env import FrodoEnv


class TestEnv(unittest.TestCase):

    def test_env_str(self):
        configuration = NonCallableMock(spec_set=[])
        env = FrodoEnv('myenv', configuration, ENV1=5, ENV2='asdasd')
        bash_env = str(env).split(' ')
        self.assertEqual(len(bash_env), 2)
        self.assertIn('ENV1="5"', bash_env)
        self.assertIn('ENV2="asdasd"', bash_env)

    def test_env_as_dict(self):
        configuration = NonCallableMock(spec_set=[])
        env = FrodoEnv('myenv', configuration, ENV1=5, ENV2=True)
        for k, v in env.as_dict().iteritems():
            print v
            self.assertTrue(isinstance(v, str) or isinstance(v, unicode))