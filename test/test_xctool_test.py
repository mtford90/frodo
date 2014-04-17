import unittest
from mock import MagicMock

from xctool_test import XCToolTest, XCToolError


class TestXCToolTest(unittest.TestCase):
    def test_default_path(self):
        test = XCToolTest(None, None, None)
        self.assertEqual(test.xctool_path, XCToolTest.default_xc_tool_path)
        test = XCToolTest(None, None, None, xctool_path='blah')
        self.assertEqual(test.xctool_path, 'blah')


# noinspection PyProtectedMember
class TestXCCoolTestOnlyParam(unittest.TestCase):
    def test_target(self):
        test = XCToolTest(None, None, target='target')
        self.assertEqual('target', test._construct_only())

    def test_target_class(self):
        test = XCToolTest(None, None, target='target', test_class='class')
        self.assertEqual('target:class', test._construct_only())

    def test_target_class_method(self):
        test = XCToolTest(None, None, target='target', test_class='class', test_method='method')
        self.assertEqual('target:class/method', test._construct_only())

    def test_target_method_throws_error(self):
        test = XCToolTest(None, None, target='target', test_method='method')
        self.assertRaises(XCToolError, test._construct_only)


# noinspection PyProtectedMember
class XCToolTestBuild(unittest.TestCase):

    def test_execute(self):
        test = XCToolTest(None, None, None)
        stdout, stderr, return_code = test._execute("echo 'hello stderr' >&2; echo 'hello stdout'; False")
        self.assertIn('hello stderr', stderr)
        self.assertIn('hello stdout', stdout)
        self.assertEqual(1, return_code)

    def test_build_success(self):
        test = XCToolTest(None, None, None)
        test._execute = MagicMock(return_value=('', '', 0))
        self.assertTrue(test._build())

    def test_build_failure(self):
        test = XCToolTest(None, None, None)
        test._execute = MagicMock(return_value=('', '', 1))
        self.assertFalse(test._build())