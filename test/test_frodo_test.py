import unittest

from mock import MagicMock

from configuration import Configuration
from runner.frodo_env import FrodoEnv
from runner.frodo_precondition import FrodoPrecondition
from runner.frodo_test import FrodoTest


# noinspection PyProtectedMember
from runner.xctool_config import XCToolConfig
from runner.xctool_test import XCToolTest


class TestFrodoTestResolution(unittest.TestCase):
    def test_resolve_env_success(self):
        config = Configuration()
        mock_env = MagicMock()
        env_name = 'myenv'
        config.environs[env_name] = mock_env
        precon = FrodoTest('name', config, cmd='True', env=env_name)
        self.assertFalse(precon._resolve_env())
        self.assertEqual(precon.env, mock_env)

    def test_resolve_env_failure(self):
        config = Configuration()
        precon = FrodoTest('name', config, cmd='True', env='myenv')
        self.assertTrue(precon._resolve_env())

    def test_resolve_config_success(self):
        config = Configuration()
        mock_config = MagicMock()
        config_name = 'myconfig'
        config.configs[config_name] = mock_config
        precon = FrodoTest('name', config, cmd='True', config=config_name)
        self.assertFalse(precon._resolve_config())
        self.assertEqual(precon.config, mock_config)

    def test_resolve_config_failure(self):
        config = Configuration()
        precon = FrodoTest('name', config, cmd='True', config='myconfig')
        self.assertTrue(precon._resolve_config())

    def test_resolve_precondition_success(self):
        config = Configuration()
        mock_precond = MagicMock()
        precond_name = 'myprecond'
        config.preconditions[precond_name] = mock_precond
        precon = FrodoTest('name', config, cmd='True', precondition=precond_name)
        self.assertFalse(precon._resolve_preconditions())
        self.assertEqual(1, len(precon.preconditions))
        self.assertEqual(precon.preconditions[0], mock_precond)

    def test_resolve_preconditions_success(self):
        config = Configuration()
        mock_precond_1 = MagicMock()
        precond_name_1 = 'myprecond1'
        mock_precond_2 = MagicMock()
        precond_name_2 = 'myprecond2'
        config.preconditions[precond_name_1] = mock_precond_1
        config.preconditions[precond_name_2] = mock_precond_2
        precon = FrodoTest('name', config, cmd='True', preconditions=[precond_name_1, precond_name_2])
        self.assertFalse(precon._resolve_preconditions())
        self.assertEqual(2, len(precon.preconditions))
        self.assertIn(mock_precond_1, precon.preconditions)
        self.assertIn(mock_precond_2, precon.preconditions)

    def test_resolve_precondition_failure(self):
        config = Configuration()
        precon = FrodoTest('name', config, cmd='True', precondition='myprecond')
        self.assertTrue(precon._resolve_preconditions())


# noinspection PyProtectedMember
class TestFrodoTestInit(unittest.TestCase):
    def test_init(self):
        test = FrodoTest('name', MagicMock())
        self.assertFalse(test.errors)
        self.assertFalse(test.success)
        self.assertFalse(test.has_run)
        self.assertFalse(test.tests)

    def test_has_run(self):
        test = FrodoTest('name', MagicMock())
        test.success = False
        self.assertTrue(test.has_run)
        test.success = True
        self.assertTrue(test.has_run)

    def test_env(self):
        mock_env = MagicMock(spec_set=FrodoEnv)
        mock_env_as_dict = {'ENVVAR': 'VAL'}
        mock_env.as_dict = MagicMock(return_value=mock_env_as_dict)
        test = FrodoTest('name', MagicMock(), env=mock_env)
        self.assertEqual(mock_env_as_dict, test._get_env())


# noinspection PyProtectedMember
class TestFrodoTestPreconditionCheck(unittest.TestCase):
    def test_success(self):
        config = MagicMock()
        precond = FrodoPrecondition('precon1', config, cmd='True')
        test = FrodoTest('name', config, cmd='True')
        setattr(test, 'preconditions', [precond])
        self.assertFalse(test._failed_preconditions())

    def test_failure(self):
        config = MagicMock()
        precond = FrodoPrecondition('precon1', config, cmd='False')
        test = FrodoTest('name', config)
        setattr(test, 'preconditions', [precond])
        result = test._failed_preconditions()
        self.assertTrue(result)
        self.assertIn('precon1', [x.name for x in result])

    def test_multiple_with_failure(self):
        config = MagicMock()
        commands = ['True', 'False', 'True', 'False']
        preconditions \
            = [FrodoPrecondition('precon%d' % i, config, cmd=v) for i, v in enumerate(commands)]
        test = FrodoTest('name', config)
        setattr(test, 'preconditions', preconditions)
        result = test._failed_preconditions()
        self.assertEqual(2, len(result))
        self.assertIn('precon1', [x.name for x in result])
        self.assertIn('precon3', [x.name for x in result])


# noinspection PyProtectedMember
class TestFrodoTestXCToolCall(unittest.TestCase):
    def test_xc_tool_call(self):
        mock_env = MagicMock(spec_set=FrodoEnv)
        mock_env_as_dict = {'ENVVAR': 'VAL'}
        mock_env.as_dict = MagicMock(return_value=mock_env_as_dict)
        mock_configuration = MagicMock(spec_set=Configuration)
        mock_config = MagicMock(spec=XCToolConfig)
        mock_config.workspace = 'workspace'
        mock_config.scheme = 'scheme'
        mock_config.sdk = 'sdk'
        kwargs = {
            'env': mock_env,
            'target': 'test-target',
            'config': mock_config
        }
        xc_test = self.assertXCToolCallCorrect(kwargs, mock_config, mock_configuration)
        self.assertFalse(xc_test.test_class)
        self.assertFalse(xc_test.test_method)

    def test_xc_tool_call_with_class_and_method(self):
        mock_env = MagicMock(spec_set=FrodoEnv)
        mock_env_as_dict = {'ENVVAR': 'VAL'}
        mock_env.as_dict = MagicMock(return_value=mock_env_as_dict)
        mock_configuration = MagicMock(spec_set=Configuration)
        mock_config = MagicMock(spec=XCToolConfig)
        mock_config.workspace = 'workspace'
        mock_config.scheme = 'scheme'
        mock_config.sdk = 'sdk'
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


class TestFrodoTestRun(unittest.TestCase):
    def test_does_not_run_with_failed_preconditions(self):
        config = MagicMock()
        precond = FrodoPrecondition('precon1', config)

        def run():
            precond.code = 1
            precond.stdout = ''
            precond.stderr = 'bleurgh'

        precond.run = MagicMock(side_effect=run)
        test = FrodoTest('name', config)
        setattr(test, 'preconditions', [precond])
        test.run()
        self.assertTrue(test.errors)

    def test_calls_run_on_xc_test_if_preconditions_pass(self):
        config = MagicMock()
        precond = FrodoPrecondition('precon1', config)

        def run():
            precond.code = 0
            precond.stdout = 'awesome'
            precond.stderr = ''

        precond.run = MagicMock(side_effect=run)
        test = FrodoTest('name', config)
        setattr(test, 'preconditions', [precond])
        mock_xc_test = MagicMock(spec_set=XCToolTest)
        mock_xc_test_run = MagicMock()
        mock_xc_test.run = mock_xc_test_run
        test._construct_xc_test = MagicMock(return_value=mock_xc_test)
        test.run()
        self.assertFalse(test.errors)
        mock_xc_test_run.assert_called_once_with()

    def test_analyse_success(self):
        config = MagicMock()
        test = FrodoTest('name', config)
        mock_test = MagicMock()
        mock_test.succeeded = True
        test.tests = [mock_test, mock_test]
        self.assertFalse(test.success)
        test._analyse()
        self.assertTrue(test.success)

    def test_analyse_failure(self):
        config = MagicMock()
        test = FrodoTest('name', config)
        success_mock_test = MagicMock()
        success_mock_test.succeeded = True
        fail_mock_test = MagicMock()
        fail_mock_test.succeeded = False
        test.tests = [success_mock_test, fail_mock_test]
        self.assertFalse(test.success)
        test._analyse()
        self.assertFalse(test.success)
