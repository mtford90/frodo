import logging
import unittest

from runner.xctool_parser import XCToolParser, ParseError


logger = logging.getLogger(__name__)


class TestXCToolOneFailedExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_parse_simple(self):
        raw = '''
        {
              "exceptions": [
                {
                  "lineNumber": 31,
                  "reason": "failed - No implementation for \\"-[FrodoTestTests testExample]\\"",
                  "filePathInProject": "/Users/mtford/Playground/frodo/test/integration/FrodoTest/FrodoTestTests/FrodoTestTests.m"
                }
              ],
              "methodName": "testExample",
              "output": "",
              "result": "failure",
              "totalDuration": 0.003446042537689209,
              "timestamp": 1397595706.418641,
              "event": "end-test",
              "test": "-[FrodoTestTests testExample]",
              "className": "FrodoTestTests",
              "succeeded": false
        }
        '''
        parser = XCToolParser([raw])
        parser.parse()
        self.assertOneFailedExampleParsedCorrectly(parser)

    def test_parse_one_failed_example(self):
        with open('data/one_failed_example.json') as f:
            parser = XCToolParser(f)
            parser.parse()
        self.assertOneFailedExampleParsedCorrectly(parser)

    def test_too_many_json_err(self):
        broken_lines = ['{"key":"val' for _ in range(0, XCToolParser.max_json_err)]
        parser = XCToolParser(broken_lines)
        self.assertRaises(ParseError, parser.parse)

    def assertOneFailedExampleParsedCorrectly(self, parser):
        self.assertFalse(parser.json_errors)
        self.assertEqual(len(parser.tests), 1)
        test = parser.tests[0]
        self.assertEqual(test.duration, 0.003446042537689209)
        self.assertEqual(test.result, test.RESULT_FAILURE)
        self.assertEqual(test.class_name, 'FrodoTestTests')
        self.assertEqual(test.method_name, 'testExample')
        self.assertFalse(test.succeeded)
        self.assertEqual(len(test.exceptions), 1)
        exception = test.exceptions[0]
        self.assertEqual(exception.line_number, 31)
        self.assertEqual(exception.reason, 'failed - No implementation for "-[FrodoTestTests testExample]"')
        self.assertEqual(exception.file_path,
                         '/Users/mtford/Playground/frodo/test/integration/FrodoTest/FrodoTestTests/FrodoTestTests.m')

