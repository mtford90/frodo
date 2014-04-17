import unittest
from mock import MagicMock
from frodo_precondition import FrodoPrecondition


class TestPrecondition(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        cmd = 'True'
        precon = FrodoPrecondition('name', MagicMock(), cmd=cmd)
        self.assertEqual(precon.code, None)
        self.assertEqual(precon.stdout, None)
        self.assertEqual(precon.stderr, None)
        self.assertFalse(precon.executed)
        self.assertFalse(precon.succeeded)
        self.assertEqual(precon.cmd, cmd)

    def test_simple_success(self):
        cmd = 'True'
        precon = FrodoPrecondition('name', MagicMock(), cmd=cmd)
        precon.run()
        self.assertTrue(precon.executed)
        self.assertTrue(precon.succeeded)

    def test_simple_failure(self):
        cmd = 'False'
        precon = FrodoPrecondition('name', MagicMock(), cmd=cmd)
        precon.run()
        self.assertTrue(precon.executed)
        self.assertFalse(precon.succeeded)

    def test_run_twice_should_raise_exception(self):
        cmd = 'False'
        precon = FrodoPrecondition('name', MagicMock(), cmd=cmd)
        precon.run()
        self.assertRaises(AssertionError, precon.run)

    def test_validate_success(self):
        cmd = 'False'
        precon = FrodoPrecondition('name', MagicMock(), cmd=cmd)
        self.assertFalse(precon.validate())

    def test_validate_failure(self):
        """validation failure if no cmd passed"""
        precon = FrodoPrecondition('name', MagicMock())
        self.assertTrue(precon.validate())