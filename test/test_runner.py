import unittest

from mock import MagicMock

from runner.runner import Runner


# noinspection PyProtectedMember
class TestRunner(unittest.TestCase):
    def test_init(self):
        configuration = MagicMock()
        runner = Runner(configuration)
        self.assertTrue(runner.configuration, configuration)

    def test_run(self):
        test_1 = MagicMock()
        dummy_1 = ['dummy', 'test', 'results', 'for', 'test1']
        test_1.run = MagicMock(return_value=dummy_1)
        test_2 = MagicMock()
        dummy_2 = ['dummy', 'test', 'results', 'for', 'test2']
        test_2.run = MagicMock(return_value=dummy_2)

    def test_default_reporter(self):
        configuration = MagicMock()
        runner = Runner(configuration)
        self.assertEqual(runner._reporter_class, runner.default_reporter_class)