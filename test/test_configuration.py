import os
import unittest


class TestConfigurationExampleSpec(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ['FRODO_CONF'] = 'spec.yaml'
        cls.conf = __import__('configuration')

    @classmethod
    def tearDownClass(cls):
        os.unsetenv('FRODO_CONF')

    def test_parse_configs(self):
        config = self.conf.configs['myconfig']
        self.assertEqual(config.workspace, 'Mosayc.xcworkspace')
        self.assertEqual(config.scheme, 'Mosayc')
        self.assertEqual(config.sdk, 'iphonesimulator7.1')

    def test_parse_environs(self):
        env = self.conf.environs['myenv']
        self.assertEqual(env.runningUnitTests, True)
        self.assertEqual(env.runningBehaviourTests, True)

    def test_parse_preconds(self):
        precon = self.conf.preconditions['myprecond']
        self.assertEqual(precon.cmd, 'echo hello')

    def test_parse_tests(self):
        test = self.conf.tests['mytest']
        env = self.conf.environs['myenv']
        myconfig = self.conf.configs['myconfig']
        myprecond = self.conf.preconditions['myprecond']
        self.assertEqual(test.target, 'Unit Tests')
        self.assertEqual(test.test_case, 'InviteFriendsToAlbumDataSourceTestCase')
        self.assertEqual(test.env, env)
        self.assertEqual(test.config, myconfig)
        self.assertListEqual([myprecond], test.preconditions)

    def test_parse_frodo(self):
        self.assertEqual(self.conf.all_preconditions, True)
        self.assertEqual(self.conf.working_dir, './')



    def test_precondition(self):
        precon = self.conf.preconditions['myprecond']
        self.assertFalse(precon.executed)
        self.assertFalse(precon.succeeded)
        precon.run()
        self.assertIn('hello', precon.stdout)
        self.assertEqual(0, precon.code)
        self.assertTrue(precon.executed)
        self.assertTrue(precon.succeeded)

