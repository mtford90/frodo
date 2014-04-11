import os

import sys

import yaml


class ConfigurationError(Exception):
    def __init__(self, errors=None, *args, **kwargs):
        super(ConfigurationError, self).__init__(*args, **kwargs)
        self.errors = errors


class FrodoConfigBase(object):
    required_attr = ()

    def __init__(self, name, **kwargs):
        super(FrodoConfigBase, self).__init__()
        self.name = name
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def validate(self):
        errors = []
        for attr in self.required_attr:
            if not hasattr(self, attr):
                errors += {self.name: errors}
        return errors

    def resolve(self, configuration):
        pass


class Config(FrodoConfigBase):
    required_attr = 'workspace', 'scheme', 'sdk'


class Test(FrodoConfigBase):
    required_attr = 'target', 'config'

    def resolve(self, configuration):
        errors = []
        if hasattr(self, 'env'):
            env_name = self.env
            try:
                # noinspection PyAttributeOutsideInit
                self.env = configuration.environs[env_name]
            except KeyError:
                errors += {env_name: 'env declaration doesnt exist'}
        conf_name = self.config
        assert hasattr(self, 'config'), 'config should have been validated'
        try:
            # noinspection PyAttributeOutsideInit
            self.config = configuration.configs[conf_name]
        except KeyError:
            errors += {conf_name: 'conf declaration doesnt exist'}
        return errors


class Environment(FrodoConfigBase):
    pass


class Configuration(object):
    default_conf_loc = 'spec.example.yaml'

    def __init__(self):
        self.path = os.getenv('FRODO_CONF', self.default_conf_loc)
        super(Configuration, self).__init__()
        self.environs = {}
        self.configs = {}
        self.tests = {}
        errors = self.parse()
        if errors:
            raise ConfigurationError(errors=errors, message='Unable to parse config file')
        errors = self.resolve()
        if errors:
            raise ConfigurationError(errors=errors, message='Resolution error')
        errors = self.validate()
        if errors:
            raise ConfigurationError(errors=errors, message='Config is invalid')

    def parse(self):
        """Perform initial parse of yaml into native python"""
        errors = []
        with open(self.path) as f:
            data = yaml.safe_load(f)
        for name in data:
            datum = data[name]
            n = len(datum)
            if not n == 1:
                errors += {name: 'should only have one type'}
                continue
            typ = datum.keys()[0]
            conf = datum[typ]
            if typ == 'env':
                self.environs[name] = Environment(name, **conf)
            elif typ == 'config':
                self.configs[name] = Config(name, **conf)
            elif typ == 'test':
                self.tests[name] = Test(name, **conf)
            else:
                errors += {typ: 'unknown type'}
        return errors

    def resolve(self):
        """Check env and config references exist"""
        errors = []
        for _, test in self.tests.iteritems():
            errors += test.resolve(self)
        return errors

    def validate(self):
        """Check for missing keys"""
        errors = []
        for _, spec in self.tests.iteritems():
            errors += spec.validate()
        for _, spec in self.configs.iteritems():
            errors += spec.validate()
        return errors


sys.modules[__name__] = Configuration()