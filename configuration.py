import os
# import sys

import yaml

from runner.frodo_env import FrodoEnv
from runner.frodo_precondition import FrodoPrecondition
from runner.frodo_test import FrodoTest
from runner.xctool_config import XCToolConfig


class Configuration(object):
    default_conf_loc = 'spec.example.yaml'
    default_opts = {
        'all_preconditions': False,
        'working_dir': './'
    }
    type_maps = {

    }

    def __init__(self):
        super(Configuration, self).__init__()
        for k, v in self.default_opts.iteritems():
            self.__setattr__(k, v)
        self._items = {}
        self._raw = None

    def _item_lazy_access(self, key):
        """lazy instantiation of configuration _items dict"""
        d = self._items.get(key)
        if not d:
            d = {}
            self._items[key] = d
        return d

    @property
    def environs(self):
        return self._item_lazy_access('environs')

    @property
    def configs(self):
        return self._item_lazy_access('configs')

    @property
    def tests(self):
        return self._item_lazy_access('tests')

    @property
    def preconditions(self):
        return self._item_lazy_access('preconditions')

    def load(self, raw=None):
        if not raw:
            path = os.getenv('FRODO_CONF', self.default_conf_loc)
            with open(path, 'r') as f:
                errors = self.parse(f)
        else:
            errors = self.parse(raw)
        if errors:
            raise ConfigurationError(errors=errors, message='Unable to parse config file')
        errors = self.resolve()
        if errors:
            raise ConfigurationError(errors=errors, message='Resolution error')
        errors = self.validate()
        if errors:
            raise ConfigurationError(errors=errors, message='Config is invalid')

    def parse(self, raw_or_file):
        """Perform initial parse of yaml into native python"""
        errors = {}
        self._raw = yaml.load(raw_or_file)
        for name in self._raw:
            datum = self._raw[name]
            n = len(datum)
            if (not name == 'frodo') and not n == 1:
                errors[name] = {'too_many_types': datum.keys()}
                continue
            typ = datum.keys()[0]
            conf = datum[typ]
            if typ == 'env':
                self.environs[name] = FrodoEnv(name, self, **conf)
            elif typ == 'config':
                self.configs[name] = XCToolConfig(name, self, **conf)
            elif typ == 'test':
                self.tests[name] = FrodoTest(name, self, **conf)
            elif typ == 'precondition':
                self.preconditions[name] = FrodoPrecondition(name, self, **conf)
            elif name == 'frodo':
                frodo_errs = self.parse_system_conf(datum)
                if frodo_errs:
                    errors[name] = frodo_errs
            else:
                errors[typ] = 'unknown type'
        return errors

    def parse_system_conf(self, frodo_conf):
        """best efforts at parsing frodo config"""
        errors = {}
        frodo_items = []
        try:
            frodo_items = frodo_conf.items()
        except AttributeError:
            errors += 'must be a dictionary'
        finally:
            opts = dict(self.default_opts.items() + frodo_items)
            expected = set(self.default_opts.keys())
            unexpected = set(opts) - expected
            for k, v in opts.iteritems():
                if k in expected:
                    setattr(self, k, v)
            if unexpected:
                errors['unexpected_fields'] = list(unexpected)
            return errors

    def resolve(self):
        """resolve any references in each config item
        e.g. map test object onto its config and env"""
        errors = {}
        for name, spec in self._items.iteritems():
            assert hasattr(spec, 'resolve'), 'Does %s:%s descend from FrodoBase?' % (name, spec)
            spec_errors = spec.resolve()
            if spec_errors:
                errors[name] = spec_errors
        return errors

    def validate(self):
        """Check for missing keys"""
        errors = {}
        for name, spec in self._items.iteritems():
            assert hasattr(spec, 'validate'), 'Does %s:%s descend from FrodoBase?' % (name, spec)
            spec_errors = spec.validate()
            if spec_errors:
                errors[name] = spec_errors
        return errors

        # sys.modules[__name__] = Configuration()


class ConfigurationError(Exception):
    def __init__(self, errors=None, message=None):
        super(ConfigurationError, self).__init__(message)
        self.errors = errors