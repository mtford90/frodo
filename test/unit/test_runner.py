import unittest

from mock import MagicMock, NonCallableMock, Mock

from runner.runner import Runner


# noinspection PyProtectedMember
class TestRunner(unittest.TestCase):
    def test_init(self):
        configuration = NonCallableMock(spec_set=[])
        runner = Runner(configuration)
        self.assertTrue(runner.configuration, configuration)

    def test_run(self):
        test_1 = NonCallableMock(spec_set=['name', 'run'], name='test_1', run=Mock())
        test_2 = NonCallableMock(spec_set=['name', 'run'], name='test_2', run=Mock())
        configuration = NonCallableMock(spec_set=['tests'], tests={test_1.name: test_1, test_2.name: test_2})
        runner = Runner(configuration)
        mock_reporter = NonCallableMock(spec_set=['report'], report=MagicMock())
        runner._get_reporter = Mock(return_value=mock_reporter)
        runner.run()
        test_1.run.assert_called_once_with()
        test_2.run.assert_called_once_with()
        mock_reporter.report.assert_called_once_with()

    def test_default_reporter(self):
        configuration = NonCallableMock(spec_set=[])
        runner = Runner(configuration)
        self.assertEqual(runner._get_reporter_class(), runner.default_reporter_class)

