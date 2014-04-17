from reporter.simple import SimpleReporter


class Runner(object):
    default_reporter_class = SimpleReporter
    """entry point for running tests"""

    def __init__(self, configuration):
        """configuration must have passed validation and resolution"""
        super(Runner, self).__init__()
        self.configuration = configuration

    @property
    def _reporter_class(self):
        return self.default_reporter_class

    def run(self):
        return {test: test.run() for test in self.configuration.tests}