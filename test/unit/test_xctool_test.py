import unittest
import subprocess

from mock import MagicMock

from runner.xctool_test import XCToolTest, XCToolError, BuildError, RunError


class TestXCToolTest(unittest.TestCase):
    def test_default_path(self):
        test = XCToolTest(None, None, None, None)
        self.assertEqual(test.xctool_path, XCToolTest.default_xc_tool_path)
        test = XCToolTest(None, None, None, None, xctool_path='blah')
        self.assertEqual(test.xctool_path, 'blah')

    def test_default_log_paths(self):
        test = XCToolTest(None, None, None, None)
        self.assertEqual(test.default_run_log_stderr, test.log_path_run_stderr)
        self.assertEqual(test.default_run_log_stdout, test.log_path_run_stdout)
        self.assertEqual(test.default_build_log_stderr, test.log_path_build_stderr)
        self.assertEqual(test.default_build_log_stdout, test.log_path_build_stdout)


# noinspection PyProtectedMember
class TestXCCoolTestOnlyParam(unittest.TestCase):
    def test_target(self):
        test = XCToolTest(None, None, None, target='target')
        self.assertEqual('target', test._construct_only())

    def test_target_class(self):
        test = XCToolTest(None, None, None, target='target', test_class='class')
        self.assertEqual('target:class', test._construct_only())

    def test_target_class_method(self):
        test = XCToolTest(None, None, None, target='target', test_class='class', test_method='method')
        self.assertEqual('target:class/method', test._construct_only())

    def test_target_method_throws_error(self):
        test = XCToolTest(None, None, None, target='target', test_method='method')
        self.assertRaises(XCToolError, test._construct_only)


# noinspection PyProtectedMember
class XCToolTestExecute(unittest.TestCase):
    def test_io(self):
        test = XCToolTest(None, None, None, None)
        stdout, stderr, return_code = test._execute("echo 'hello stderr' >&2; echo 'hello stdout'; False")
        self.assertIn('hello stderr', stderr)
        self.assertIn('hello stdout', stdout)
        self.assertEqual(1, return_code)

    def test_env(self):
        """all subprocesses should use 'env' parameter passed via constructor"""
        mock_process = MagicMock()
        mock_process.communicate = MagicMock(return_value=('', ''))
        mock_process.return_code = 0
        mock_Popen = MagicMock(return_value=mock_process)
        stashed_Popen = subprocess.Popen
        subprocess.Popen = mock_Popen
        mock_env = {'ENV_VAR': 'VAL'}
        test = XCToolTest(None, None, None, None, env=mock_env)
        test._execute('True')
        try:
            self.assertTrue(mock_Popen.call_count)
            for args, kwargs in mock_Popen.call_args_list:
                env = kwargs.get('env', None)
                self.assertTrue(env)
                self.assertDictEqual(env, mock_env)
        except AssertionError:
            raise
        finally:
            subprocess.Popen = stashed_Popen


# noinspection PyProtectedMember
class XCToolTestBuildCommand(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workspace = 'workspace'
        cls.scheme = 'scheme'
        cls.target = 'target'
        cls.test_method = 'test_method'
        cls.test_class = 'test_class'
        test = XCToolTest(workspace=cls.workspace,
                          scheme=cls.scheme,
                          target=cls.target,
                          sdk='something',
                          test_method=cls.test_method,
                          test_class=cls.test_class)
        cls.cmd = test._construct_build_cmd()

    def test_workspace(self):
        self.assertIn(self.workspace, self.cmd)

    def test_scheme(self):
        self.assertIn(self.scheme, self.cmd)

    def test_target(self):
        self.assertIn(self.target, self.cmd)

    # def test_test_method(self):
    #     self.assertIn(self.test_method, self.cmd)
    #
    # def test_test_class(self):
    #     self.assertIn(self.test_class, self.cmd)


# noinspection PyProtectedMember
class XCToolTestBuild(unittest.TestCase):
    def test_build_success(self):
        test = XCToolTest(None, None, None, None)
        test._execute = MagicMock(return_value=('', '', 0))
        test._build()

    def test_build_failure(self):
        test = XCToolTest(None, None, None, None)
        test._execute = MagicMock(return_value=('', '', 1))
        self.assertRaises(BuildError, test._build)


class XCToolTestRun(unittest.TestCase):
    def test_run_if_build_fails(self):
        test = XCToolTest(None, None, None, None)
        test._build = MagicMock(side_effect=BuildError)
        self.assertRaises(BuildError, test.run)

    def _test_run_success(self, code):
        test = XCToolTest(None, None, None, None)
        test._execute = MagicMock(return_value=('', '', code))
        test._build = MagicMock()
        mock_parser = MagicMock()
        dummy_tests = ['dummy', 'test', 'results']
        mock_parser.tests = dummy_tests
        test._get_parser = MagicMock(return_value=mock_parser)
        self.assertEqual(dummy_tests, test.run())

    def test_run_success(self):
        """should parse stdout and return the test objects"""
        self._test_run_success(0)

    def test_run_success_1(self):
        self._test_run_success(1)

    def test_run_failure(self):
        test = XCToolTest(None, None, None, None)
        test._execute = MagicMock(return_value=('', '', 2))
        test._build = MagicMock()
        self.assertRaises(RunError, test.run)

