import logging
import os
import subprocess

from xctool_parser import XCToolParser


logger = logging.getLogger(__name__)


class XCToolError(Exception):
    """generic XCTool failure"""
    pass


class BuildError(XCToolError):
    """unable to build and hence can't execute tests"""
    pass


class RunError(XCToolError):
    """unable to run tests for whatever reason"""
    pass


class XCToolTest(object):
    parser_class = XCToolParser
    default_xc_tool_path = os.path.dirname(os.path.realpath(__file__)) + '/../bin/xctool'
    default_build_log_stdout = '/tmp/frodo-build.stdout.log'
    default_build_log_stderr = '/tmp/frodo-build.stderr.log'
    default_run_log_stdout = '/tmp/frodo-run.stdout.log'
    default_run_log_stderr = '/tmp/frodo-run.stderr.log'
    build_tests_cmd = '{xctool_path} ' \
                      '-workspace {workspace} ' \
                      '-scheme {scheme} ' \
                      'build-tests'

    run_tests_cmd = '{xctool_path} ' \
                    '-workspace {workspace} ' \
                    '-scheme {scheme} ' \
                    'run-tests -only "{only}" ' \
                    '-sdk {sdk} -reporter json-stream'

    def __init__(self, workspace, scheme, sdk, target, test_class=None, test_method=None, xctool_path=None, env=None):
        super(XCToolTest, self).__init__()
        self._xctool_path = xctool_path
        self.workspace = workspace
        self.scheme = scheme
        self.sdk = sdk
        self.target = target
        self.test_class = test_class
        self.test_method = test_method
        self.env = env

    @property
    def xctool_path(self):
        return self._xctool_path or self.default_xc_tool_path

    @property
    def log_path_build_stdout(self):
        return self.default_build_log_stdout

    @property
    def log_path_build_stderr(self):
        return self.default_build_log_stderr

    @property
    def log_path_run_stdout(self):
        return self.default_run_log_stdout

    @property
    def log_path_run_stderr(self):
        return self.default_run_log_stderr

    def _construct_only(self):
        only = self.target
        if self.test_class:
            only += ':' + self.test_class
        if self.test_method:
            if not self.test_class:
                raise XCToolError('need to specify a test class if specifying a test method')
            only += '/' + self.test_method
        return only

    def _execute(self, cmd):
        logger.debug("Executing '%s'" % cmd)
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, env=self.env)
        stdout, stderr, return_code = process.communicate() + (process.returncode,)
        return stdout, stderr, return_code

    def _construct_build_cmd(self):
        build_cmd = self.build_tests_cmd.format(xctool_path=self.xctool_path,
                                                workspace=self.workspace,
                                                scheme=self.scheme)
        return build_cmd

    def _build(self):
        build_cmd = self._construct_build_cmd()
        stdout, stderr, return_code = self._execute(build_cmd)
        # test_cmd = self.bash_cmd.format(xctool=self.default_xc_tool,
        stdout_log = self.log_path_build_stdout
        logger.debug('Writing %s' % stdout_log)
        with open(stdout_log, 'w') as f:
            f.write(stdout)
        stderr_log = self.log_path_build_stderr
        logger.debug('Writing %s' % stderr_log)
        with open(stderr_log, 'w') as f:
            f.write(stderr)
        if return_code:
            excp_msg = 'Build failed with exit code %d' % return_code
            logger.fatal((excp_msg + '. See %s and %s for more details.') % (
                stdout_log, stderr_log))
            raise BuildError(excp_msg)
        else:
            logger.info('Build successful')

    def _get_parser_class(self):
        return self.parser_class

    def _get_parser(self, stream):
        parser_class = self._get_parser_class()
        return parser_class(stream)

    def _parse(self, stdout):
        parser = self._get_parser(stdout.split('\n'))
        parser.parse()
        return parser.tests

    def _construct_run_cmd(self):
        bash_cmd = self.run_tests_cmd.format(xctool_path=self.xctool_path,
                                             workspace=self.workspace,
                                             scheme=self.scheme,
                                             only=self._construct_only(),
                                             sdk=self.sdk)
        return bash_cmd

    def run(self):
        self._build()
        bash_cmd = self._construct_run_cmd()
        stdout, stderr, return_code = self._execute(bash_cmd)
        stdout_log = self.default_run_log_stdout
        stderr_log = self.default_run_log_stderr
        logger.debug('Writing %s' % stdout_log)
        with open(stdout_log, 'w') as f:
            f.write(stdout)
        logger.debug('Writing %s' % stderr_log)
        with open(stderr_log, 'w') as f:
            f.write(stderr)
        if return_code > 1:
            logger.fatal('Testing failed with exit code %d. See %s and %s for more details.' % (
                return_code, stdout_log, stderr_log))
            raise RunError()
        else:
            logger.info('Tests ran successfully.')
            return self._parse(stdout)

