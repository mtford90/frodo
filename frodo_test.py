import json
import logging
import os
import subprocess

from frodo_base import FrodoBase


Logger = logging.getLogger('frodo')


class Test(FrodoBase):
    """Representation of an xcode test"""
    required_attr = 'target', 'config'

    max_err = 10

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

    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.relevant = []

    @property
    def has_run(self):
        return len(self.relevant) > 0

    def _build(self):
        build_cmd = self.build_tests_cmd.format(xctool=self.default_xc_tool,
                                                workspace=self.config.workspace,
                                                scheme=self.config.scheme)
        Logger.debug("Executing '%s'" % build_cmd)
        env = self._kwargs.get('env', None)
        if env:
            env = env.as_dict()
        process = subprocess.Popen(build_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   env=env, shell=True)
        stdout, stderr = process.communicate()
        return_code = process.returncode
        Logger.debug('XCTool exited with return code %s' % return_code)
        # test_cmd = self.bash_cmd.format(xctool=self.default_xc_tool,
        stdout_log = '/tmp/frodo-build.stdout.log'
        stderr_log = '/tmp/frodo-build.stderr.log'
        Logger.info('Writing %s' % stdout_log)
        with open(stdout_log, 'w') as f:
            f.write(stdout)
        Logger.info('Writing %s' % stderr_log)
        with open(stderr_log, 'w') as f:
            f.write(stderr)
        if not return_code in [0, 1]:
            Logger.fatal('Build failed. See logs for more info.')
        else:
            Logger.info('Build successful')

    def run(self):
        env = self._kwargs.get('env', None)
        if env:
            env = env.as_dict()
        Logger.info("Running test '%s'" % self.name)
        wd = self.configuration.working_dir
        Logger.info("Changing to directory: '%s'" % wd)
        os.chdir(wd)
        self._build()
        bash_cmd = self.bash_cmd.format(xctool=self.default_xc_tool, workspace=self.config.workspace,
                                        scheme=self.config.scheme, only=self._construct_only(), sdk=self.config.sdk)
        Logger.debug("Executing '%s'" % bash_cmd)
        process = subprocess.Popen(bash_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   env=env, shell=True)
        stdout, stderr = process.communicate()
        return_code = process.returncode
        stdout_log = '/tmp/frodo-run.stdout.log'
        stderr_log = '/tmp/frodo-run.stderr.log'
        Logger.info('Writing %s' % stdout_log)
        with open(stdout_log, 'w') as f:
            f.write(stdout)
        Logger.info('Writing %s' % stderr_log)
        with open(stderr_log, 'w') as f:
            f.write(stderr)
        if not return_code in [0, 1]:
            Logger.fatal('Test failed. See logs for more info.')
        else:
            Logger.info('Tests ran successfully.')
        parsed_json = self._parse_stdout(stdout)
        self._process_results(parsed_json)

    def _construct_only(self):
        only = self.target
        if hasattr(self, 'test_case'):
            only += ':' + self.test_case
        if hasattr(self, 'test'):
            only += '/' + self.test
        return only

    def _process_results(self, parsed_json):
        for parsed in parsed_json:
            event = parsed.get('event', None)
            if event:
                if event == 'end-test':
                    Logger.debug('Found relevant xctool result: %s' % parsed)
                    self.relevant.append(parsed)

    def _parse_stdout(self, stdout):
        Logger.info('Parsing output from XCTool')
        err_count = 0
        parsed_json = []
        for json_string in stdout.split('\n'):
            try:
                parsed_json.append(json.loads(json_string))
            except ValueError:
                Logger.warn('Unable to parse \'%s\'', json_string)
                err_count += 1
                if err_count >= self.max_err:
                    Logger.error('Too many errors')
        return parsed_json

    def _resolve_env(self):
        errors = []
        if 'env' in self._kwargs:
            env_name = self.env
            try:
                # noinspection PyAttributeOutsideInit
                self._kwargs['env'] = self.configuration.environs[env_name]
            except KeyError:
                errors += {env_name: 'env declaration doesnt exist'}
        return errors

    def _resolve_config(self):
        errors = []
        conf_name = self.config
        assert 'config' in self._kwargs, 'config should have been validated'
        try:
            # noinspection PyAttributeOutsideInit
            self._kwargs['config'] = self.configuration.configs[conf_name]
        except KeyError:
            errors += {conf_name: 'conf declaration doesnt exist'}
        return errors

    def resolve(self):
        errors = []
        errors += self._resolve_env()
        errors += self._resolve_config()
        errors += self._resolve_preconditions()
        return errors

    def _resolve_preconditions(self):
        errors = []
        preconditions = self._kwargs.get('precondition') or self._kwargs.get('preconditions')
        resolved_preconditions = []
        if preconditions:
            try:
                for precond_name in preconditions:
                    try:
                        precond = self.configuration.preconditions[precond_name]
                        resolved_preconditions.append(precond)
                    except KeyError:
                        errors += {precond_name: 'No such precondition'}
            except TypeError:
                precond_name = preconditions
                try:
                    resolved_preconditions.append(self.configuration.preconditions[precond_name])
                except KeyError:
                    errors += {precond_name: 'No such precondition'}
            self._kwargs['preconditions'] = resolved_preconditions
        return errors