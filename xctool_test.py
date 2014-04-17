__author__ = 'mtford'


class XCToolTest(object):
    default_xc_tool = '/Users/mtford/Scripts/XCTool/build/Products/Release/xctool'

    build_tests_cmd = '{xctool} ' \
                      '-workspace {workspace} ' \
                      '-scheme {scheme} ' \
                      'build-tests'

    bash_cmd = '{xctool} ' \
               '-workspace {workspace} ' \
               '-scheme {scheme} ' \
               'run-tests -only "{only}" ' \
               '-sdk {sdk} -reporter json-stream'

    def __init__(self):
        super(XCToolTest, self).__init__()

    def _construct_only(self):
        only = self.target
        if hasattr(self, 'test_case'):
            only += ':' + self.test_case
        if hasattr(self, 'test'):
            only += '/' + self.test
        return only


        # def _build(self):
        #     build_cmd = self.build_tests_cmd.format(xctool=self.default_xc_tool,
        #                                             workspace=self.config.workspace,
        #                                             scheme=self.config.scheme)
        #     Logger.debug("Executing '%s'" % build_cmd)
        #     env = self._kwargs.get('env', None)
        #     if env:
        #         env = env.as_dict()
        #     process = subprocess.Popen(build_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        #                                env=env, shell=True)
        #     stdout, stderr = process.communicate()
        #     return_code = process.returncode
        #     Logger.debug('XCTool exited with return code %s' % return_code)
        #     # test_cmd = self.bash_cmd.format(xctool=self.default_xc_tool,
        #     stdout_log = '/tmp/frodo-build.stdout.log'
        #     stderr_log = '/tmp/frodo-build.stderr.log'
        #     Logger.info('Writing %s' % stdout_log)
        #     with open(stdout_log, 'w') as f:
        #         f.write(stdout)
        #     Logger.info('Writing %s' % stderr_log)
        #     with open(stderr_log, 'w') as f:
        #         f.write(stderr)
        #     if not return_code in (0, 1):
        #         Logger.fatal('Build failed. See logs for more info.')
        #     else:
        #         Logger.info('Build successful')
        #
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

