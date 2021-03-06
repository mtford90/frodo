from unittest import TestCase

from mock import NonCallableMock, Mock

from configuration import Configuration
from runner.frodo_env import FrodoEnv
from runner.frodo_precondition import FrodoPrecondition
from runner.frodo_test import FrodoTest
from runner.xctool_config import XCToolConfig


class TestConfiguration(TestCase):
    # noinspection PyUnresolvedReferences
    def test_defaults(self):
        configuration = Configuration()
        self.assertFalse(configuration.all_preconditions)
        self.assertEqual(configuration.working_dir, './')

    def test_default_config_path(self):
        configuration = Configuration()
        self.assertEquals(configuration.config_path, configuration.default_config_path)

    def test_config_path(self):
        mock_path = 'dfdsf'
        configuration = Configuration(mock_path)
        self.assertEquals(configuration.config_path, mock_path)


class TestConfiguration_ParseErrors(TestCase):
    def test_too_many_types(self):
        raw = '''
               myenv:
                 env:
                   x: 1
                   y: 2
                 test:
                   z: 6
                   p: 9
        '''
        configuration = Configuration()
        errors = configuration.parse(raw)
        print errors
        self.assertDictEqual({'myenv': {'too_many_types': ['test', 'env']}}, errors)

    def test_unknown_options(self):
        raw = '''
               frodo:
                 all_preconditions: True
                 working_dir: /Users/mtford/
                 something_random: 5
        '''
        configuration = Configuration()
        errors = configuration.parse(raw)
        print errors
        self.assertDictEqual({'frodo': {'unexpected_fields': ['something_random']}}, errors)


class TestConfigurationParseSystem(TestCase):
    # noinspection PyUnresolvedReferences
    def test_all(self):
        raw = '''
               frodo:
                 all_preconditions: True
                 working_dir: /Users/mtford/
        '''
        configuration = Configuration()
        errors = configuration.parse(raw)
        self.assertTrue(configuration.all_preconditions)
        self.assertEqual(configuration.working_dir, '/Users/mtford/')
        self.assertFalse(errors)


class TestConfigurationParseFrodoBase(TestCase):
    @classmethod
    def setUpClass(cls):
        raw = '''
               myenv:
                 env:
                   x: 1
               myconf:
                 config:
                   x: 1
               mytest:
                 test:
                   x: 1
               myprecondition:
                 precondition:
                   x: 1
              '''
        cls.configuration = Configuration()
        cls.errors = cls.configuration.parse(raw)

    def test_no_errors(self):
        self.assertFalse(self.errors)

    def assertParsedCorrectly(self, attr, expected_type, key):
        self.assertTrue(hasattr(self.configuration, attr))
        d = getattr(self.configuration, attr)
        self.assertIn(key, d)
        self.assertEqual(1, len(d))
        base = d[key]
        self.assertIsInstance(base, expected_type)
        self.assertTrue(base.x, 1)
        self.assertEqual(base.configuration, self.configuration)

    def test_environ(self):
        self.assertParsedCorrectly(key='myenv', expected_type=FrodoEnv, attr='environs')

    def test_xctool_config(self):
        self.assertParsedCorrectly(key='myconf', expected_type=XCToolConfig, attr='configs')

    def test_tests(self):
        self.assertParsedCorrectly(key='mytest', expected_type=FrodoTest, attr='tests')

    def test_preconds(self):
        self.assertParsedCorrectly(key='myprecondition', expected_type=FrodoPrecondition, attr='preconditions')


class TestConfiguration_Resolve(TestCase):
    def test_calls_with_no_errors(self):
        configuration = Configuration()
        mock_env = NonCallableMock(spec_set=['resolve'])
        mock_env.resolve = Mock(return_value=None)
        items = {'env': {'m1': mock_env, 'm2': mock_env,
                         'm3': mock_env}}
        configuration._items = items
        errors = configuration.resolve()
        self.assertEqual(3, mock_env.resolve.call_count)
        self.assertFalse(errors)

    def test_calls_with_errors(self):
        configuration = Configuration()
        error = {'error': 'description of error'}
        items = {
            'env': {
                'm1': NonCallableMock(spec_set=['resolve'], resolve=Mock(return_value=None)),
                'm2': NonCallableMock(spec_set=['resolve'], resolve=Mock(return_value=None)),
                'm3': NonCallableMock(spec_set=['resolve'], resolve=Mock(return_value=error))
            }
        }
        configuration._items = items
        errors = configuration.resolve()
        for mock in items['env'].values():
            mock.resolve.assert_called_once_with()
        self.assertDictEqual({'m3': error}, errors)


class TestConfiguration_Validation(TestCase):
    def test_calls_with_no_errors(self):
        configuration = Configuration()
        mock_env = NonCallableMock(spec_set=['validate'])
        mock_env.validate = Mock(return_value=None)
        items = {'env': {'m1': mock_env, 'm2': mock_env,
                         'm3': mock_env}}
        configuration._items = items
        errors = configuration.validate()
        self.assertEqual(3, mock_env.validate.call_count)
        self.assertFalse(errors)

    def test_calls_with_errors(self):
        configuration = Configuration()
        error = {'error': 'description of error'}
        items = {
            'env': {
                'm1': NonCallableMock(spec_set=['validate'], validate=Mock(return_value=None)),
                'm2': NonCallableMock(spec_set=['validate'], validate=Mock(return_value=None)),
                'm3': NonCallableMock(spec_set=['validate'], validate=Mock(return_value=error))
            }
        }
        configuration._items = items
        errors = configuration.validate()
        for mock in items['env'].values():
            mock.validate.assert_called_once_with()
        self.assertDictEqual({'m3': error}, errors)