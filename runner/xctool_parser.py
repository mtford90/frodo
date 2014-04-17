import json
import logging

KEY_TEST_CLASS = 'className'
KEY_TEST_METHOD = 'methodName'
KEY_SUCCEEDED = 'succeeded'
KEY_EXCEPTIONS = 'exceptions'
KEY_RESULT = 'result'
KEY_DURATION = 'totalDuration'
KEY_EVENT = 'event'

KEY_EXCEPTION_REASON = 'reason'
KEY_EXCEPTION_FILE_PATH = 'filePathInProject'
KEY_EXCEPTION_LINE_NUMBER = 'lineNumber'

EVENT_END_TEST = 'end-test'

logger = logging.getLogger(__name__)


class ParseError(Exception):
    def __init__(self, message=None, cause=None):
        self.cause = cause
        self.message = message


class XCToolTestResultException(object):
    def __init__(self, **raw):
        super(XCToolTestResultException, self).__init__()
        self.reason = raw[KEY_EXCEPTION_REASON]
        self.file_path = raw[KEY_EXCEPTION_FILE_PATH]
        self.line_number = raw[KEY_EXCEPTION_LINE_NUMBER]


class XCToolTestResult(object):
    RESULT_FAILURE = 'failure'

    def __init__(self, **raw):
        super(XCToolTestResult, self).__init__()
        self.class_name = raw[KEY_TEST_CLASS]
        self.method_name = raw[KEY_TEST_METHOD]
        self.succeeded = raw[KEY_SUCCEEDED]
        self.exceptions = [XCToolTestResultException(**x) for x in raw[KEY_EXCEPTIONS]]
        self.result = raw[KEY_RESULT]
        self.duration = raw[KEY_DURATION]


class XCToolParser(object):
    max_json_err = 10

    def __init__(self, stream):
        super(XCToolParser, self).__init__()
        self._stream = stream
        self.tests = []
        self.json_errors = []

    def parse(self):
        line_num = 0
        for line in self._stream:
            line_num += 1
            self._parse_line(line, line_num)

    def _parse_line(self, line, line_num):
        try:
            d = json.loads(line)
        except (TypeError, ValueError) as e:
            logger.error("Unable to parse output from XCTool \'%s\' at line %d" % (line, line_num))
            self.json_errors += [{'line_num': line_num, 'line': line, 'exception': e}]
            if len(self.json_errors) >= self.max_json_err:
                raise ParseError(message='Too many json errors', cause=self.json_errors)
            return
        typ = d.get(KEY_EVENT, None)
        if typ == EVENT_END_TEST:
            try:
                self.tests.append(XCToolTestResult(**d))
            except KeyError, e:
                raise ParseError(message='Problem with XCTool output at line %d' % line_num, cause=e)
