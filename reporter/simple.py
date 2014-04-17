import logging

__author__ = 'mtford'

logger = logging.getLogger('SimpleReporter')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)


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
        for test_name, test in self.configuration.tests.iteritems():
            msg = '%s ' % test_name
            if test.success:
                msg += 'passed\n'
            else:
                msg += 'failed\n'
            total_tests = len(test.tests)
            failures = [x for x in test.tests if not x.succeeded]
            successes = [x for x in test.tests if x.succeeded]
            total_failures = len(failures)
            total_success = total_tests - total_failures
            if successes:
                msg += '\t%d/%d test(s) passed:' % (total_success, total_tests)
                for xc_tool_test_result in successes:
                    test_class = xc_tool_test_result.class_name
                    test_method = xc_tool_test_result.method_name
                    msg += '\n\t\t - %s:%s/%s' % (test.target, test_class, test_method)
                if failures:
                    msg += '\n\n'
            if failures:
                msg += '\t%d/%d test(s) failed:' % (total_failures, total_tests)
                for xc_tool_test_result in failures:
                    test_class = xc_tool_test_result.class_name
                    test_method = xc_tool_test_result.method_name
                    msg += '\n\t\t - %s:%s/%s' % (test.target, test_class, test_method)
                logger.info(msg)