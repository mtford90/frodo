import unittest

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
class XCToolTestBuild(unittest.TestCase):
    def test_execute(self):
        test = XCToolTest(None, None, None, None)
        stdout, stderr, return_code = test._execute("echo 'hello stderr' >&2; echo 'hello stdout'; False")
        self.assertIn('hello stderr', stderr)
        self.assertIn('hello stdout', stdout)
        self.assertEqual(1, return_code)

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

    def test_run_success(self):
        """should parse stdout and return the test objects"""
        test = XCToolTest(None, None, None, None)
        test._execute = MagicMock(return_value=('', '', 0))
        mock_parser = MagicMock()
        dummy_tests = ['dummy', 'test', 'results']
        mock_parser.tests = dummy_tests
        test._get_parser = MagicMock(return_value=mock_parser)
        self.assertEqual(dummy_tests, test.run())

    def test_run_failure(self):
        test = XCToolTest(None, None, None, None)
        test._execute = MagicMock(return_value=('', '', 1))
        test._build = MagicMock()
        self.assertRaises(RunError, test.run)

