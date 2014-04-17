import logging
import subprocess

from runner.frodo_base import FrodoBase


Logger = logging.getLogger('frodo')


class FrodoPrecondition(FrodoBase):
    required_attr = ('cmd',)

    def __init__(self, *args, **kwargs):
        super(FrodoPrecondition, self).__init__(*args, **kwargs)
        self.code = None
        self.stdout = None
        self.stderr = None

    @property
    def executed(self):
        return not self.code is None

    @property
    def succeeded(self):
        return self.code == 0

    def run(self):
        assert not self.executed, 'Precondition has already run'
        if Logger.isEnabledFor(logging.DEBUG):
            Logger.debug("Executing: '%s'" % self.cmd)
        env = None
        try:
            env = self.env.as_dict()
        except AttributeError:
            pass
        process = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, env=env)
        self.stdout, self.stderr = process.communicate()
        self.code = process.returncode

    def resolve(self):
        errors = []
        if 'env' in self._kwargs:
            env_name = self.env
            try:
                # noinspection PyAttributeOutsideInit
                self._kwargs['env'] = self.configuration.environs[env_name]
            except KeyError:
                errors += {env_name: 'env declaration doesnt exist'}
        return errors