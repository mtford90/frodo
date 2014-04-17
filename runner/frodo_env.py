from runner.frodo_base import FrodoBase


class FrodoEnv(FrodoBase):
    """Representation of bash environment that commands+tests should run under"""

    def __str__(self):
        """e.g:
        ENV_VAR="SOMETHING" ANOTHER_ENV_VAR="SOMETHING ELSE"
        """
        bash_env_str = ''
        for k, v in self._kwargs.iteritems():
            bash_env_str += '%s="%s" ' % (k, v)
        return bash_env_str.strip()

    # TODO: This could probs be implemented as special methods: __iter__, __getattr__ etc
    def as_dict(self):
        """Same as super, but ensure all values are strings"""
        d = super(FrodoEnv, self).as_dict()
        return {k: str(v) for k, v in d.iteritems()}

