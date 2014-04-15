KEY_TEST_CLASS = 'className'
KEY_TEST_METHOD = 'methodName'
KEY_SUCCEEDED = 'succeeded'
KEY_EXCEPTIONS = 'exceptions'
KEY_RESULT = 'result'
KEY_DURATION = 'totalDuration'

KEY_EXCEPTION_REASON = 'reason'
KEY_EXCEPTION_FILE_PATH = 'filePathInProject'
KEY_EXCEPTION_LINE_NUMBER = 'lineNumber'


class XCToolException(object):
    def __init__(self, reason, file_path, line_number):
        super(XCToolException, self).__init__()
        self.reason = reason
        self.file_path = file_path
        self.line_number = line_number


class XCToolTest(object):
    def __init__(self, class_name, method_name, succeeded, exceptions, result, duration):
        super(XCToolTest, self).__init__()
        self.class_name = class_name
        self.method_name = method_name
        self.succeeded = succeeded
        self.exceptions = exceptions
        self.result = result
        self.duration = duration


class XCToolParser(object):
    def __init__(self, stream):
        super(XCToolParser, self).__init__()


    # def _parse_line(self, line):
    #     print line
    #     for line in stream:
    #         self._parse_line(line)
    #
