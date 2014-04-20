import unittest

from mock import NonCallableMock, patch, Mock

from runner.frodo_precondition import FrodoPrecondition


class TestPreconditionRun(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.patcher = patch('subprocess.Popen',
                            new_callable=Mock,
                            spec_set=['communicate', 'returncode'],
                            communicate=Mock(return_value=('out', 'err')),
                            returncode=0)
        cls.patcher.start()

    def subprocessesFail(self):
        self._changeProcessReturnCode(1)

    def _changeProcessReturnCode(self, returncode):
        self.patcher.stop()
        self.patcher.kwargs['returncode'] = returncode
        self.patcher.start()

    def subprocessesSuceed(self):
        self._changeProcessReturnCode(0)

    def test_init(self):
        configuration = NonCallableMock(spec_set=[])
        cmd = NonCallableMock(spec_set=[])
        precon = FrodoPrecondition('name', configuration, cmd=cmd)
        self.assertEqual(precon.code, None)
        self.assertEqual(precon.stdout, None)
        self.assertEqual(precon.stderr, None)
        self.assertFalse(precon.executed)
        self.assertFalse(precon.succeeded)
        self.assertEqual(precon.cmd, cmd)

    def test_simple_success(self):
        self.subprocessesSuceed()
        configuration = NonCallableMock(spec_set=[])
        precon = FrodoPrecondition('name', configuration, cmd=NonCallableMock(spec_set=[]))
        precon.run()
        self.assertTrue(precon.executed)
        self.assertTrue(precon.succeeded)

    def test_simple_failure(self):
        self.subprocessesFail()
        configuration = NonCallableMock(spec_set=[])
        precon = FrodoPrecondition('name', configuration, cmd=NonCallableMock(spec_set=[]))
        precon.run()
        self.assertTrue(precon.executed)
        self.assertFalse(precon.succeeded)

    def test_run_twice_should_raise_exception(self):
        configuration = NonCallableMock(spec_set=[])
        precon = FrodoPrecondition('name', configuration, cmd=NonCallableMock(spec_set=[]))
        precon.run()
        self.assertRaises(AssertionError, precon.run)

    def test_validate_success(self):
        configuration = NonCallableMock(spec_set=[])
        precon = FrodoPrecondition('name', configuration, cmd=NonCallableMock(spec_set=[]))
        self.assertFalse(precon.validate())

    def test_validate_failure(self):
        """validation failure if no cmd passed"""
        configuration = NonCallableMock(spec_set=[])
        precon = FrodoPrecondition('name', configuration)
        self.assertTrue(precon.validate())

    def test_stdout(self):
        configuration = NonCallableMock(spec_set=[])
        precon = FrodoPrecondition('name', configuration, cmd=NonCallableMock(spec_set=[]))
        precon.run()
        self.assertTrue(precon.stdout)
        self.assertIn('out', precon.stdout)

    def test_stderr(self):
        configuration = NonCallableMock(spec_set=[])
        precon = FrodoPrecondition('name', configuration, cmd=NonCallableMock(spec_set=[]))
        precon.run()
        self.assertTrue(precon.stderr)
        self.assertIn('err', precon.stderr)


class TestPreconditionEnv(unittest.TestCase):
    @patch('subprocess.Popen', new_callable=Mock, spec_set=['communicate', 'returncode'],
           communicate=Mock(return_value=('out', 'err')), returncode=0)
    def test_env(self, Popen):
        var_val = 'hello there!'
        env_dict = {'VAR': var_val}
        env = Mock(spec_set=['as_dict'], as_dict=Mock(return_value=env_dict))
        precon = FrodoPrecondition('name', NonCallableMock(spec_set=[]), cmd=NonCallableMock(spec_set=[]), env=env)
        precon.run()
        self.assertEqual(1, Popen.call_count)
        args, kwargs = Popen.call_args
        self.assertDictEqual(kwargs['env'], env_dict)


    @patch('subprocess.Popen')  # Ensure never called
    def test_resolve_success(self, _):
        env_name = 'myenv'
        mock_env = NonCallableMock(spec_set=[])
        config = NonCallableMock(spec_set=['environs'], environs={env_name: mock_env})
        precon = FrodoPrecondition('name', config, cmd=NonCallableMock(spec_set=[]), env=env_name)
        self.assertFalse(precon.resolve())
        self.assertEqual(precon.env, mock_env)

    @patch('subprocess.Popen')  # Ensure never called
    def test_resolve_failure(self, _):
        config = NonCallableMock(spec_set=['environs'], environs={})
        precon = FrodoPrecondition('name', config, cmd=NonCallableMock(spec_set=[]), env='myenv')
        self.assertTrue(precon.resolve())