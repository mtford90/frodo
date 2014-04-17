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
        test_1.name = 'test_1'
        test_1.run = MagicMock()
        test_2 = MagicMock()
        test_2.name = 'test_2'
        test_2.run = MagicMock()
        configuration = MagicMock()
        configuration.tests = [test_1, test_2]
        runner = Runner(configuration)
        mock_reporter = MagicMock()
        mock_reporter.report = MagicMock()
        runner._get_reporter = MagicMock(return_value=mock_reporter)
        runner.run()
        test_1.run.assert_called_once_with()
        test_2.run.assert_called_once_with()
        mock_reporter.report.assert_called_once_with()

    def test_default_reporter(self):
        configuration = MagicMock()
        runner = Runner(configuration)
        self.assertEqual(runner._get_reporter_class(), runner.default_reporter_class)

