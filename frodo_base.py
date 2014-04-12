import logging
import subprocess
Logger = logging.getLogger('frodo')


class FrodoBase(object):
    """Base validation & behaviours"""
    required_attr = ()

    def __init__(self, name, configuration, **kwargs):
        super(FrodoBase, self).__init__()
        self.name = name
        self.configuration = configuration
        self._kwargs = kwargs  # cordon off frodo attributes from super attributes

    def __getattr__(self, item):
        try:
            return self._kwargs[item]
        except KeyError:
            raise AttributeError(item)

    def validate(self):
        errors = []
        for attr in self.required_attr:
            if not hasattr(self, attr):
                errors += {self.name: errors}
        return errors

    def resolve(self):
        pass

    def as_dict(self):
        return self._kwargs


class XCToolConfig(FrodoBase):
    """XCTool configuration"""
    required_attr = 'workspace', 'scheme', 'sdk'


class Env(FrodoBase):
    """Representation of bash environment that commands+tests should run under"""

    def __str__(self):
        """e.g:
        ENV_VAR="SOMETHING" ANOTHER_ENV_VAR="SOMETHING ELSE"
        """
        bash_env_str = ''
        for k, v in self._kwargs.iteritems():
            bash_env_str += '%s="%s" ' % (k, v)
        return bash_env_str.strip()

    def as_dict(self):
        d = super(Env, self).as_dict()
        return {k: str(v) for k, v in d.iteritems()}


class Precondition(FrodoBase):
    required_attr = ('cmd',)

    def __init__(self, *args, **kwargs):
        super(Precondition, self).__init__(*args, **kwargs)
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
        process = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, shell=True)
        self.stdout, self.stderr = process.communicate()
        self.code = process.returncode
