import os
import unittest


class ConfigurationTestValid(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ['FRODO_CONF'] = 'spec.yaml'
        cls.conf = __import__('configuration')

    @classmethod
    def tearDownClass(cls):
        os.unsetenv('FRODO_CONF')

    def test_parse_configs(self):
        self.assertDictEqual({
            'myconfig': {
                'workspace': 'Mosayc.xcworkspace',
                'scheme': 'Mosayc',
                'sdk': 'iphonesimulator7.1'
            }
        }, self.conf.configs)

    def test_parse_environs(self):
        self.assertDictEqual({
            'myenv': {
                'runningUnitTests': True,
                'runningBehaviourTests': True
            }
        }, self.conf.environs)

    def test_parse_tests(self):
        self.assertDictEqual({
            'mytest': {
                'target': 'Unit Tests',
                'test_case': 'InviteFriendsToAlbumDataSourceTestCase',
                'env': self.conf.environs['myenv'],
                'config': self.conf.configs['myconfig']
            }
        }, self.conf.tests)


class ConfigurationTestParseError(unittest.TestCase):  # TODO

    def test(self):
        self.assertTrue(False)


class ConfigurationTestResolutionError(unittest.TestCase):  # TODO

    def test(self):
        self.assertTrue(False)


class ConfigurationTestValidationError(unittest.TestCase):  # TODO

    def test(self):
        self.assertTrue(False)