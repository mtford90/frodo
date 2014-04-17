import logging

from frodo_base import FrodoBase
from xctool_test import XCToolTest


Logger = logging.getLogger('frodo')


class FrodoTest(FrodoBase):
    required_attr = 'target', 'config'

    def __init__(self, *args, **kwargs):
        super(FrodoTest, self).__init__(*args, **kwargs)
        self.errors = []
        self.success = None
        self.tests = []

    @property
    def has_run(self):
        return self.success is not None

    def _resolve_env(self):
        errors = []
        if 'env' in self._kwargs:
            env_name = self.env
            try:
                # noinspection PyAttributeOutsideInit
                self._kwargs['env'] = self.configuration.environs[env_name]
            except KeyError:
                errors += [{env_name: 'env declaration doesnt exist'}]
        return errors

    def _resolve_config(self):
        errors = []
        conf_name = self.config
        assert 'config' in self._kwargs, 'config should have been validated'
        try:
            # noinspection PyAttributeOutsideInit
            self._kwargs['config'] = self.configuration.configs[conf_name]
        except KeyError:
            errors += [{conf_name: 'conf declaration doesnt exist'}]
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
            precond_name = preconditions
            try:
                resolved_preconditions.append(self.configuration.preconditions[precond_name])
            except KeyError:
                errors += [{precond_name: 'No such precondition'}]
            except TypeError:
                for precond_name in preconditions:
                    try:
                        precond = self.configuration.preconditions[precond_name]
                        resolved_preconditions.append(precond)
                    except KeyError:
                        errors += [{precond_name: 'No such precondition'}]
            self._kwargs['preconditions'] = resolved_preconditions
        return errors

    def _get_env(self):
        """best efforts at deriving a bash environment"""
        env = None
        try:
            env = self.env.as_dict()
        except AttributeError:
            pass
        return env

    def _run(self):
        test = self._construct_xc_test()
        self.tests = test.run()

    def _analyse(self):
        self.success = all(x.succeeded for x in self.tests)

    def _construct_xc_test(self):
        test = XCToolTest(workspace=self.config.workspace,
                          scheme=self.config.scheme,
                          sdk=self.config.sdk,
                          target=self.target,
                          test_class=getattr(self, 'test_class', None),
                          test_method=getattr(self, 'test_method', None),
                          env=self._get_env())
        return test

    def run(self):
        failed_preconds = self._failed_preconditions()
        if failed_preconds:
            self.errors += failed_preconds
        else:
            self._run()
            self._analyse()

    def _failed_preconditions(self):
        errors = []
        if hasattr(self, 'preconditions'):
            for precon in self.preconditions:
                precon.run()
                if not precon.succeeded:
                    errors.append(precon)
        return errors