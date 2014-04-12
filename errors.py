class ConfigurationError(Exception):
    def __init__(self, errors=None, message=None):
        super(ConfigurationError, self).__init__(message)
        self.errors = errors