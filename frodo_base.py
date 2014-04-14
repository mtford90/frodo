# import collections
#
#
# def update(d, u):
#     for k, v in u.iteritems():
#         if isinstance(v, collections.Mapping):
#             r = update(d.get(k, {}), v)
#             d[k] = r
#         else:
#             d[k] = u[k]
#     return d


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
        errors = {}
        for attr in self.required_attr:
            if not hasattr(self, attr):
                errors[attr] = errors
        return errors

    def resolve(self):
        pass

    def as_dict(self):
        return self._kwargs
