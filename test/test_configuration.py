from unittest import TestCase

from mock import MagicMock

from configuration import Configuration
from frodo_env import FrodoEnv
from frodo_precondition import FrodoPrecondition
from frodo_test import FrodoTest
from xctool_config import XCToolConfig


class TestConfiguration_ParseErrors(TestCase):
    # noinspection PyUnresolvedReferences
    def test_defaults(self):
        configuration = Configuration()
        self.assertFalse(configuration.all_preconditions)
        self.assertEqual(configuration.working_dir, './')

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
        items = {'m1': MagicMock(spec_set=FrodoEnv), 'm2': MagicMock(spec_set=FrodoEnv),
                 'm3': MagicMock(spec_set=FrodoEnv)}
        for mock in items.values():
            mock.resolve = MagicMock(return_value=None)
        configuration._items = items
        errors = configuration.resolve()
        for mock in items.values():
            mock.resolve.assert_called_once_with()
        self.assertFalse(errors)

    def test_calls_with_errors(self):
        configuration = Configuration()
        items = {'m1': MagicMock(spec_set=FrodoEnv), 'm2': MagicMock(spec_set=FrodoEnv),
                 'm3': MagicMock(spec_set=FrodoEnv)}
        items['m1'].resolve = MagicMock(return_value=None)
        items['m2'].resolve = MagicMock(return_value=None)
        error = {'error': 'description of error'}
        items['m3'].resolve = MagicMock(return_value=error)
        configuration._items = items
        errors = configuration.resolve()
        for mock in items.values():
            mock.resolve.assert_called_once_with()
        self.assertDictEqual({'m3': error}, errors)


class TestConfiguration_Validation(TestCase):

    def test_calls_with_no_errors(self):
        configuration = Configuration()
        items = {'m1': MagicMock(spec_set=FrodoEnv), 'm2': MagicMock(spec_set=FrodoEnv),
                 'm3': MagicMock(spec_set=FrodoEnv)}
        for mock in items.values():
            mock.validate = MagicMock(return_value=None)
        configuration._items = items
        errors = configuration.validate()
        for mock in items.values():
            mock.validate.assert_called_once_with()
        self.assertFalse(errors)

    def test_calls_with_errors(self):
        configuration = Configuration()
        items = {'m1': MagicMock(spec_set=FrodoEnv), 'm2': MagicMock(spec_set=FrodoEnv),
                 'm3': MagicMock(spec_set=FrodoEnv)}
        items['m1'].validate = MagicMock(return_value=None)
        items['m2'].validate = MagicMock(return_value=None)
        error = {'error': 'description of error'}
        items['m3'].validate = MagicMock(return_value=error)
        configuration._items = items
        errors = configuration.validate()
        for mock in items.values():
            mock.validate.assert_called_once_with()
        self.assertDictEqual({'m3': error}, errors)