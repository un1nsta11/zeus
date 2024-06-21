# ======================================================================================================================
# COMMAND EXECUTOR FOR WINDOWS OS
# Dependencies: None
# ======================================================================================================================
from subprocess import Popen, PIPE, TimeoutExpired
import logging

__all__ = [
    "cmd",
    "exec_cmd"
]

from typing import Tuple, Union


def exec_cmd(
        command,
        timeout=None,
        work_dir=None,
        verbose=False,
) -> Union[Tuple[int, Union[bytes, str], Union[bytes, str]], int]:
    """
    Run command with timeout (seconds) and get error code
    Args:
        command: str() command to execute with arguments
        timeout: seconds
        work_dir: from which directory it should be launched
        verbose: if True, return (ret_code, stdout, stderr), if False return code
    Returns:
        Error Level: 5 access is denied; 10: timeout expired
    """
    ret_code = 0
    outs = ''
    errs = ''
    try:
        proc = Popen(command, stdout=PIPE, stderr=PIPE, cwd=work_dir)

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

    logging.info(f'Command: {command}; ErrorLevel: {ret_code}')
    if verbose:
        return ret_code, outs, errs
    else:
        return ret_code


def cmd(command, background=False, timeout=None, work_dir=None,
        verbose=False, verbose_logging=True, info_logging=True) -> Union[
    Tuple[int, Union[bytes, str], Union[bytes, str]], int]:
    """
    Execute <cmd> and return it is returned code
    Args:
        :param command: string, cmd to execute
        :param background: if true don't wait for exit
        :param timeout: seconds
        :param work_dir: from which directory it should be launched
        :param verbose: if True, return (ret_code, stdout, stderr), if False return code
        :param verbose_logging: return full output with errors
        :return: exit code
    """
    if info_logging:
        logging.info(f'CMD: {command}')

    proc = Popen(command, stdout=PIPE, stderr=PIPE, cwd=work_dir)
    ret_code = 0
    outs = ''
    errs = ''
    if not background:
        try:
            outs, errs = proc.communicate(timeout=timeout)
            try:
                ret_code = proc.returncode
                outs = outs.replace(b'\r', b'').replace(b'\n', b'')
                errs = errs.replace(b'\r', b'').replace(b'\n', b'')
                # logging.debug("Stdout: {}".format(outs))
                # logging.debug("Stderr: {}".format(errs))
            except UnicodeDecodeError:
                pass
        except TimeoutExpired:
            ret_code = 5
            logging.warning('Timeout expired. Set return code to {}'.format(ret_code))
    if verbose_logging:
        logging.info(f'Command: {command}; ErrorLevel: {ret_code}')

    if verbose:
        return ret_code, outs, errs
    else:
        return ret_code


def _encode(byte_object):
    if isinstance(byte_object, str):
        encoded = byte_object.encode('utf-8')
        return encoded
    else:
        return byte_object
