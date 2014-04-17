import logging

from frodo_base import FrodoBase


Logger = logging.getLogger('frodo')


class FrodoTest(FrodoBase):
    """Representation of an xcode test"""
    required_attr = 'target', 'config'

    def __init__(self, *args, **kwargs):
        super(FrodoTest, self).__init__(*args, **kwargs)

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