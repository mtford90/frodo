import logging
import subprocess

logger = logging.getLogger(__name__)


class XCToolError(Exception):
    pass


class XCToolTest(object):
    default_xc_tool_path = '/Users/mtford/Scripts/XCTool/build/Products/Release/xctool'
    default_build_log_stdout = '/tmp/frodo-build.stdout.log'
    default_build_log_stderr = '/tmp/frodo-build.stderr.log'
    build_tests_cmd = '{xctool_path} ' \
                      '-workspace {workspace} ' \
                      '-scheme {scheme} ' \
                      'build-tests'

    bash_cmd = '{xctool_path} ' \
               '-workspace {workspace} ' \
               '-scheme {scheme} ' \
               'run-tests -only "{only}" ' \
               '-sdk {sdk} -reporter json-stream'

    def __init__(self, workspace, scheme, target, test_class=None, test_method=None, xctool_path=None):
        super(XCToolTest, self).__init__()
        self._xctool_path = xctool_path
        self.workspace = workspace
        self.scheme = scheme
        self.target = target
        self.test_class = test_class
        self.test_method = test_method

    @property
    def xctool_path(self):
        return self._xctool_path or self.default_xc_tool_path

    @property
    def log_path_build_stdout(self):
        return self.default_build_log_stdout

    @property
    def log_path_build_stderr(self):
        return self.default_build_log_stderr

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
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr, return_code = process.communicate() + (process.returncode,)
        return stdout, stderr, return_code

    def _build(self):
        build_cmd = self.build_tests_cmd.format(xctool_path=self._xctool_path,
                                                workspace=self.workspace,
                                                scheme=self.scheme)
        stdout, stderr, return_code = self._execute(build_cmd)
        # test_cmd = self.bash_cmd.format(xctool=self.default_xc_tool,
        stdout_log = self.log_path_build_stdout
        logger.info('Writing %s' % stdout_log)
        with open(stdout_log, 'w') as f:
            f.write(stdout)
        stderr_log = self.log_path_build_stderr
        logger.info('Writing %s' % stderr_log)
        with open(stderr_log, 'w') as f:
            f.write(stderr)
        if return_code:
            logger.fatal('Build failed with exit code %d. See %s and %s for more details.' % (
                return_code, stdout_log, stderr_log))
        else:
            logger.info('Build successful')
        success = not return_code
        return success

            # def run(self):
            #     env = self._kwargs.get('env', None)
            #     if env:
            #         env = env.as_dict()
            #     Logger.info("Running test '%s'" % self.name)
            #     wd = self.configuration.working_dir
            #     Logger.info("Changing to directory: '%s'" % wd)
            #     os.chdir(wd)
            #     self._build()
            #     bash_cmd = self.bash_cmd.format(xctool=self.default_xc_tool,
            #                                     workspace=self.config.workspace,
            #                                     scheme=self.config.scheme,
            #                                     only=self._construct_only(),
            #                                     sdk=self.config.sdk)
            #     Logger.debug("Executing '%s'" % bash_cmd)
            #     process = subprocess.Popen(bash_cmd,
            #                                stdout=subprocess.PIPE,
            #                                stderr=subprocess.PIPE,
            #                                env=env,
            #                                shell=True)
            #     stdout, stderr = process.communicate()
            #     return_code = process.returncode
            #     stdout_log = '/tmp/frodo-run.stdout.log'
            #     stderr_log = '/tmp/frodo-run.stderr.log'
            #     Logger.info('Writing %s' % stdout_log)
            #     with open(stdout_log, 'w') as f:
            #         f.write(stdout)
            #     Logger.info('Writing %s' % stderr_log)
            #     with open(stderr_log, 'w') as f:
            #         f.write(stderr)
            #     if not return_code in [0, 1]:
            #         Logger.fatal('Test failed. See logs for more info.')
            #     else:
            #         Logger.info('Tests ran successfully.')

