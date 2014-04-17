__author__ = 'mtford'


class BaseReporter(object):
    def __init__(self, configuration):
        super(BaseReporter, self).__init__()
        self.configuration = configuration

    def report(self):
        pass


class SimpleReporter(BaseReporter):
    def __init__(self, *args, **kwargs):
        super(SimpleReporter, self).__init__(*args, **kwargs)

    def report(self):
        for test in self.configuration.tests:
            msg = '%s ' % test.name
            if test.succeeded:
                msg += 'passed'
            else:
                msg += 'failed'
            print msg