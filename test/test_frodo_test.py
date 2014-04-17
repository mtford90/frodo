import unittest

from mock import MagicMock

from configuration import Configuration
from runner.frodo_precondition import FrodoPrecondition
from runner.frodo_test import FrodoTest



# noinspection PyProtectedMember
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


class TestFrodoTestInit(unittest.TestCase):
    def test_init(self):
        test = FrodoTest('name', MagicMock())
        self.assertFalse(test.errors)
        self.assertFalse(test.success)
        self.assertFalse(test.has_run)

    def test_has_run(self):
        test = FrodoTest('name', MagicMock())
        test.success = False
        self.assertTrue(test.has_run)
        test.success = True
        self.assertTrue(test.has_run)


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

