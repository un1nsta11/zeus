import os
import logging
import psutil

from logging import config
from subprocess import PIPE, Popen

logging.config.fileConfig(os.path.join(os.getcwd(), 'config', 'logconf.ini'))
logging = logging.getLogger('addons')


class ProcEx:

    def __init__(self):
        pass
