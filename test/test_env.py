import os
import unittest


class TestEnvExampleSpec(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ['FRODO_CONF'] = 'spec.yaml'
        cls.conf = __import__('configuration')

    def test_env_str(self):
        env = self.conf.environs['myenv']
        bash_env = str(env).split(' ')
        self.assertEqual(len(bash_env), 2)
        self.assertIn('runningUnitTests="True"', bash_env)
        self.assertIn('runningBehaviourTests="True"', bash_env)

    def test_env_as_dict(self):
        env = self.conf.environs['myenv']
        for k, v in env.as_dict().iteritems():
            print v
            self.assertTrue(isinstance(v, str) or isinstance(v, unicode))