import logging
import os
import sys

import yaml

from errors import ConfigurationError

from frodo_base import *
from frodo_test import Test


class Configuration(object):
    default_conf_loc = 'spec.example.yaml'
    default_opts = {
        'all_preconditions': True,
        'working_dir': './'
    }

    def __init__(self):
        self.path = os.getenv('FRODO_CONF', self.default_conf_loc)
        super(Configuration, self).__init__()
        self.environs = {}
        self.configs = {}
        self.tests = {}
        self.preconditions = {}
        self._bootstrap()
        self.init_loggers()

    def _bootstrap(self):
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
            if (not name == 'frodo') and not n == 1:
                errors += {name: 'should only have one type'}
                continue
            typ = datum.keys()[0]
            conf = datum[typ]
            if typ == 'env':
                self.environs[name] = Env(name, self, **conf)
            elif typ == 'config':
                self.configs[name] = XCToolConfig(name, self, **conf)
            elif typ == 'test':
                self.tests[name] = Test(name, self, **conf)
            elif typ == 'precondition':
                self.preconditions[name] = Precondition(name, self, **conf)
            elif name == 'frodo':
                errors += self.parse_system_conf(datum)
            else:
                errors += {typ: 'unknown type'}
        return errors

    def parse_system_conf(self, frodo_conf):
        """best efforts at parsing frodo config"""
        errors = []
        frodo_items = []
        try:
            frodo_items = frodo_conf.items()
        except AttributeError:
            errors += {'frodo': '\'frodo\' config must be a dictionary'}
        finally:
            opts = dict(self.default_opts.items() + frodo_items)
            expected = set(self.default_opts.keys())
            unexpected = set(opts) - expected
            for k, v in opts.iteritems():
                if k in expected:
                    setattr(self, k, v)
            if unexpected:
                errors += {'frodo': 'unexpected options: ' + ', '.join(unexpected)}
            return errors

    def resolve(self):
        """Check env and config references exist"""
        errors = []
        for _, test in self.tests.iteritems():
            errors += test.resolve()
        return errors

    def validate(self):
        """Check for missing keys"""
        errors = []
        for _, spec in self.tests.iteritems():
            errors += spec.validate()
        for _, spec in self.configs.iteritems():
            errors += spec.validate()
        for _, spec in self.preconditions.iteritems():
            errors += spec.validate()
        return errors

    def init_loggers(self):
        logger = logging.getLogger('frodo')
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)-15s %(levelname)-7s %(message)s [%(funcName)s (%(filename)s:%(lineno)s)]')
        ch.setFormatter(formatter)
        logger.addHandler(ch)


sys.modules[__name__] = Configuration()