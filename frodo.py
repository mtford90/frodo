import os
from configuration import Configuration
from runner.runner import Runner


class Frodo(object):
    def __init__(self, config_path=None):
        super(Frodo, self).__init__()
        self._config_path = config_path or os.environ.get('FRODO_CONF')
        self.configuration = Configuration(config_path)

    def start(self):
        self.configuration.load()
        runner = Runner(configuration=self.configuration)
        runner.run()