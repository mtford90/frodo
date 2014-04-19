import os
import unittest

from mock import MagicMock, call, Mock, NonCallableMock, patch

from configuration import Configuration
from runner.frodo_env import FrodoEnv
from runner import frodo_precondition
from runner.frodo_test import FrodoTest
from runner.xctool_config import XCToolConfig
from runner.xctool_test import XCToolTest


def mock_precond(name, succeeded):
    precond = NonCallableMock(spec_set=['name', 'succeeded', 'run'])
    precond.configure_mock(name=name, succeeded=succeeded)
    precond.run = Mock(return_value=None)
    return precond


# noinspection PyProtectedMember
class TestFrodoTestResolution(unittest.TestCase):
    def test_resolve_env_success(self):
        env = NonCallableMock(spec_set=[])
        env_name = 'myenv'
        configuration = NonCallableMock(spec_set=['environs'], environs={env_name: env})
        test = FrodoTest('name', configuration, env=env_name)
        self.assertFalse(test._resolve_env())
        self.assertEqual(test.env, env)

    def test_resolve_env_failure(self):
        configuration = NonCallableMock(spec_set=['environs'], environs={})
        test = FrodoTest('name', configuration, env='myenv')
        self.assertTrue(test._resolve_env())

    def test_resolve_config_success(self):
        config = NonCallableMock(spec_set=[])
        config_name = 'myconfig'
        configuration = NonCallableMock(spec_set=['configs'], configs={config_name: config})
        test = FrodoTest('name', configuration, config=config_name)
        self.assertFalse(test._resolve_config())
        self.assertEqual(test.config, config)

    def test_resolve_config_failure(self):
        configuration = NonCallableMock(spec_set=['configs'], configs={})
        test = FrodoTest('name', configuration, config='myconfig')
        self.assertTrue(test._resolve_config())

    def test_resolve_precondition_success(self):
        precond = NonCallableMock(spec_set=[])
        precond_name = 'myprecond'
        configuration = NonCallableMock(spec_set=['preconditions'], preconditions={precond_name: precond})
        test = FrodoTest('name', configuration, precondition=precond_name)
        self.assertFalse(test._resolve_preconditions())
        self.assertEqual(1, len(test.preconditions))
        self.assertEqual(test.preconditions[0], precond)

    def test_resolve_preconditions_success(self):
        mock_precond_1 = NonCallableMock(spec_set=[])
        precond_name_1 = 'myprecond1'
        mock_precond_2 = NonCallableMock(spec_set=[])
        precond_name_2 = 'myprecond2'
        config = NonCallableMock(spec_set=['preconditions'],
                                 preconditions={precond_name_1: mock_precond_1, precond_name_2: mock_precond_2})
        test = FrodoTest('name', config, preconditions=[precond_name_1, precond_name_2])
        self.assertFalse(test._resolve_preconditions())
        self.assertEqual(2, len(test.preconditions))
        self.assertIn(mock_precond_1, test.preconditions)
        self.assertIn(mock_precond_2, test.preconditions)

    def test_resolve_precondition_failure(self):
        config = NonCallableMock(spec_set=['preconditions'], preconditions={})
        test = FrodoTest('name', config, precondition='myprecond')
        self.assertTrue(test._resolve_preconditions())


# noinspection PyProtectedMember
class TestFrodoTestInit(unittest.TestCase):
    def test_init(self):
        test = FrodoTest('name', NonCallableMock(spec_set=[]))
        self.assertFalse(test.errors)
        self.assertFalse(test.success)
        self.assertFalse(test.has_run)
        self.assertFalse(test.tests)

    def test_has_run(self):
        test = FrodoTest('name', NonCallableMock(spec_set=[]))
        test.success = False
        self.assertTrue(test.has_run)
        test.success = True
        self.assertTrue(test.has_run)

    def test_env(self):
        mock_env = NonCallableMock(spec_set=['as_dict'])
        mock_env_as_dict = {'ENVVAR': 'VAL'}
        mock_env.as_dict = Mock(return_value=mock_env_as_dict)
        test = FrodoTest('name', NonCallableMock(spec_set=[]), env=mock_env)
        self.assertEqual(mock_env_as_dict, test._get_env())


# noinspection PyProtectedMember
class TestFrodoTestTempDir(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = NonCallableMock(spec_set=['working_dir'], working_dir='/tmp')
        os.makedirs = Mock(return_value=None)
        test = FrodoTest('blah', cls.config)
        test._mk_tmp_dir()

    def test_mk_temp_dir(self):
        # noinspection PyUnresolvedReferences
        os.makedirs.assert_called_once_with(self.config.working_dir + '/' + FrodoTest.tmp_dir_name)


# noinspection PyProtectedMember

class TestFrodoTestPreconditionCheck(unittest.TestCase):
    def test_success(self):
        config = NonCallableMock(spec_set=[])
        name = 'precond'
        precond = mock_precond(name, True)
        precond.succeeded = True
        test = FrodoTest('name', config)
        setattr(test, 'preconditions', [precond])
        self.assertFalse(test._failed_preconditions())

    def test_failure(self):
        config = NonCallableMock(spec_set=[])
        name = 'precon1'
        precond = mock_precond(name, False)
        test = FrodoTest('test-name', config)
        setattr(test, 'preconditions', [precond])
        result = test._failed_preconditions()
        self.assertTrue(result)
        self.assertIn(name, [x.name for x in result])

    def test_multiple_with_failure(self):
        config = NonCallableMock(spec_set=[])
        commands = [True, False, True, False]
        preconditions = [mock_precond('precon%d' % i, v) for i, v in enumerate(commands)]
        test = FrodoTest('name', config)
        setattr(test, 'preconditions', preconditions)
        result = test._failed_preconditions()
        self.assertEqual(2, len(result))
        self.assertIn('precon1', [x.name for x in result])
        self.assertIn('precon3', [x.name for x in result])


# noinspection PyProtectedMember
class TestFrodoTestXCToolCall(unittest.TestCase):
    def test_xc_tool_call(self):
        mock_env = NonCallableMock(spec_set=['as_dict'])
        mock_env_as_dict = {'ENVVAR': 'VAL'}
        mock_env.as_dict = Mock(return_value=mock_env_as_dict)
        mock_configuration = NonCallableMock(spec_set=[])
        mock_config = NonCallableMock(spec_set=['workspace', 'scheme', 'sdk'],
                                      workspace='workspace',
                                      scheme='scheme',
                                      sdk='sdk')
        kwargs = {
            'env': mock_env,
            'target': 'test-target',
            'config': mock_config
        }
        xc_test = self.assertXCToolCallCorrect(kwargs, mock_config, mock_configuration)
        self.assertFalse(xc_test.test_class)
        self.assertFalse(xc_test.test_method)

    def test_xc_tool_call_with_class_and_method(self):
        mock_env = NonCallableMock(spec_set=['as_dict'])
        mock_env_as_dict = {'ENVVAR': 'VAL'}
        mock_env.as_dict = Mock(return_value=mock_env_as_dict)
        mock_configuration = NonCallableMock(spec_set=[])
        mock_config = NonCallableMock(spec_set=['workspace', 'scheme', 'sdk'],
                                      workspace='workspace',
                                      scheme='scheme',
                                      sdk='sdk')
        kwargs = {
            'env': mock_env,
            'target': 'test-target',
            'config': mock_config,
            'test_class': 'test_class',
            'test_method': 'test_method'
        }
        xc_test = self.assertXCToolCallCorrect(kwargs, mock_config, mock_configuration)
        self.assertEqual(xc_test.test_class, 'test_class')
        self.assertEqual(xc_test.test_method, 'test_method')

    def assertXCToolCallCorrect(self, kwargs, mock_config, mock_configuration):
        test = FrodoTest('an-awesome-test',
                         mock_configuration,
                         **kwargs)
        xc_test = test._construct_xc_test()
        self.assertEqual(xc_test.target, 'test-target')
        self.assertEqual(xc_test.workspace, mock_config.workspace)
        self.assertEqual(xc_test.scheme, mock_config.scheme)
        self.assertEqual(xc_test.sdk, mock_config.sdk)
        return xc_test


# noinspection PyProtectedMember
class TestFrodoTestRun(unittest.TestCase):
    def test_does_not_run_with_failed_preconditions(self):
        config = NonCallableMock(spec_set=[])
        precond = mock_precond('precon1', False)
        test = FrodoTest('name', config)
        setattr(test, 'preconditions', [precond])
        test.run()
        self.assertTrue(test.errors)

    def test_calls_run_on_xc_test_if_preconditions_pass(self):
        mock_working_dir = 'mock_wd'
        configuration = NonCallableMock(spec_set=['working_dir'], working_dir=mock_working_dir)
        precond = mock_precond('precon1', True)
        test = FrodoTest('name', configuration)
        setattr(test, 'preconditions', [precond])
        mock_xc_test = NonCallableMock(spec_set=['run'])
        mock_run_xc_test = Mock(return_value=[])
        mock_xc_test.run = mock_run_xc_test
        test._construct_xc_test = Mock(return_value=mock_xc_test)
        with patch.object(os, 'chdir', new=mock_run_xc_test):
            os.chdir = mock_run_xc_test
            test.run()
            self.assertFalse(test.errors)
            # Change we change directory
            mock_run_xc_test.assert_has_calls([call(mock_working_dir), call()], any_order=False)

    def test_analyse_success(self):
        config = Mock(spec_set=[])
        test = FrodoTest('name', config)
        mock_test = Mock(spec_set=['succeeded'], succeeded=True)
        test.tests = [mock_test, mock_test]
        self.assertFalse(test.success)
        test._analyse()
        self.assertTrue(test.success)

    def test_analyse_failure(self):
        config = Mock(spec_set=[])
        test = FrodoTest('name', config)
        success_mock_test = Mock(spec_set=['succeeded'], succeeded=True)
        fail_mock_test = Mock(spec_set=['succeeded'], succeeded=False)
        test.tests = [success_mock_test, fail_mock_test]
        self.assertFalse(test.success)
        test._analyse()
        self.assertFalse(test.success)
