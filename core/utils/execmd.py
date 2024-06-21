import logging
import os

from logging import config
from subprocess import Popen, TimeoutExpired, PIPE
from time import sleep

logging.config.fileConfig(os.path.join(os.getcwd(), 'config', 'logconf.ini'))
logging = logging.getLogger('zeus')


class Cmder:

    def __init__(self, command, workdir, uptime):
        self.cmd = command
        self.workdir = workdir
        self.uptime = uptime

    def exec_cmd(self, timeout=30, verbose=False):
        """
        Run command with timeout (seconds) and get error code
        Args:
            self.command: str() command to execute with arguments
            timeout: seconds
            self.workdir: from which directory it should be launched
            verbose: if True, return (ret_code, stdout, stderr), if False return code
        Returns:
            Error Level: 5 access is denied; 10: timeout expired
        """
        sleep(self.uptime)
        ret_code = 0
        outs = ''
        errs = ''
        try:
            proc = Popen(self.cmd, stdout=PIPE, stderr=PIPE, cwd=self.workdir)

            try:
                outs, errs = proc.communicate(timeout=timeout)
                try:
                    ret_code = proc.returncode
                    outs = outs.replace(b'\r', b'').replace(b'\n', b'')
                    errs = errs.replace(b'\r', b'').replace(b'\n', b'')
                except UnicodeDecodeError:
                    pass
            except TimeoutExpired:
                ret_code = 10
                logging.warning('Timeout expired. Set return code to {}'.format(ret_code))
        except PermissionError:
            ret_code = 5
        except OSError:
            ret_code = 1

        logging.info(f'Command: {self.cmd}; error_level: {ret_code}')
        if verbose:
            return ret_code, outs, errs
        else:
            return ret_code