import logging
import os

from logging import config

logging.config.fileConfig(os.path.join(os.getcwd(), 'config', 'logconf.ini'))
logging = logging.getLogger('spider')


class HostCommands:

    def __init__(self):
        pass

    def cmd(self):
        """
        Execute command on the host machine
        :return: str() result
        """
        logging.info('Requested: remote command execution on host')

    def sysinfo(self):
        logging.info("Requested: system information")
        pass



