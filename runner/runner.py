from reporter.simple import SimpleReporter


class Runner(object):
    default_reporter_class = SimpleReporter
    """entry point for running tests"""

    def __init__(self, configuration):
        """configuration must have passed validation and resolution"""
        super(Runner, self).__init__()
        self.configuration = configuration
        self.frodo_tests = []

    def _get_reporter_class(self):
        return self.default_reporter_class

    def _get_reporter(self):
        reporter_class = self._get_reporter_class()
        reporter = reporter_class(self.configuration)
        return reporter

    def run(self):
        for test in self.configuration.tests:
            test.run()
        reporter = self._get_reporter()
        reporter.report()