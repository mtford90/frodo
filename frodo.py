import logging
import os

from configuration import Configuration
from runner.runner import Runner



class Frodo(object):
    def __init__(self, config_path=None):
        super(Frodo, self).__init__()
        self.configure_loggers()
        self._config_path = config_path or os.environ.get('FRODO_CONF')
        self.configuration = Configuration(config_path)

    @property
    def log_handler(self):
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)-15s %(levelname)-8s %(message)s [%(funcName)s (%(filename)s:%(lineno)s)]')
        ch.setFormatter(formatter)
        return ch

    def configure_loggers(self):
        loggers = map(logging.getLogger, ('runner.xctool_test', 'runner.frodo_test', 'runner.xctool_parser'))
        for logger in loggers:
            logger.setLevel(logging.DEBUG)
            logger.addHandler(self.log_handler)


    def start(self):
        self.configuration.load()
        runner = Runner(configuration=self.configuration)
        runner.run()