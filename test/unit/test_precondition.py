import unittest

from mock import NonCallableMock

from runner.frodo_env import FrodoEnv
from runner.frodo_precondition import FrodoPrecondition


class TestPreconditionRun(unittest.TestCase):

    def test_init(self):
        cmd = 'True'
        configuration = NonCallableMock(spec_set=[])
        precon = FrodoPrecondition('name', configuration, cmd=cmd)
        self.assertEqual(precon.code, None)
        self.assertEqual(precon.stdout, None)
        self.assertEqual(precon.stderr, None)
        self.assertFalse(precon.executed)
        self.assertFalse(precon.succeeded)
        self.assertEqual(precon.cmd, cmd)

    def test_simple_success(self):
        cmd = 'True'
        configuration = NonCallableMock(spec_set=[])
        precon = FrodoPrecondition('name', configuration, cmd=cmd)
        precon.run()
        self.assertTrue(precon.executed)
        self.assertTrue(precon.succeeded)

    def test_simple_failure(self):
        cmd = 'False'
        configuration = NonCallableMock(spec_set=[])
        precon = FrodoPrecondition('name', configuration, cmd=cmd)
        precon.run()
        self.assertTrue(precon.executed)
        self.assertFalse(precon.succeeded)

    def test_run_twice_should_raise_exception(self):
        cmd = 'False'
        configuration = NonCallableMock(spec_set=[])
        precon = FrodoPrecondition('name', configuration, cmd=cmd)
        precon.run()
        self.assertRaises(AssertionError, precon.run)

    def test_validate_success(self):
        cmd = 'False'
        configuration = NonCallableMock(spec_set=[])
        precon = FrodoPrecondition('name', configuration, cmd=cmd)
        self.assertFalse(precon.validate())

    def test_validate_failure(self):
        """validation failure if no cmd passed"""
        configuration = NonCallableMock(spec_set=[])
        precon = FrodoPrecondition('name', configuration)
        self.assertTrue(precon.validate())

    def test_stdout(self):
        cmd = "echo 'hello'"
        configuration = NonCallableMock(spec_set=[])
        precon = FrodoPrecondition('name', configuration, cmd=cmd)
        precon.run()
        self.assertTrue(precon.stdout)
        self.assertIn('hello', precon.stdout)

    def test_stderr(self):
        cmd = "echo hello >&2"
        configuration = NonCallableMock(spec_set=[])
        precon = FrodoPrecondition('name', configuration, cmd=cmd)
        precon.run()
        self.assertTrue(precon.stderr)
        self.assertIn('hello', precon.stderr)

    def test_stdout_and_stderr(self):
        cmd = "echo hello >&2; echo blah"
        configuration = NonCallableMock(spec_set=[])
        precon = FrodoPrecondition('name', configuration, cmd=cmd)
        precon.run()
        self.assertTrue(precon.stderr)
        self.assertIn('hello', precon.stderr)
        self.assertTrue(precon.stdout)
        self.assertIn('blah', precon.stdout)


class TestPreconditionEnv(unittest.TestCase):

    def test_env(self):
        cmd = 'echo ${VAR}'
        var_val = 'hello there!'
        configuration = NonCallableMock(spec_set=[])
        env = FrodoEnv('myenv', configuration, VAR=var_val)
        precon = FrodoPrecondition('name', configuration, cmd=cmd, env=env)
        precon.run()
        self.assertIn(var_val, precon.stdout)

    def test_resolve_success(self):
        env_name = 'myenv'
        mock_env = NonCallableMock(spec_set=[])
        config = NonCallableMock(spec_set=['environs'], environs={env_name: mock_env})
        precon = FrodoPrecondition('name', config, cmd='True', env=env_name)
        self.assertFalse(precon.resolve())
        self.assertEqual(precon.env, mock_env)

    def test_resolve_failure(self):
        config = NonCallableMock(spec_set=['environs'], environs={})
        precon = FrodoPrecondition('name', config, cmd='True', env='myenv')
        self.assertTrue(precon.resolve())