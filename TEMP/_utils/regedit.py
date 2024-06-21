# ======================================================================================================================
# REG QUERY COMMAND WRAPPER
# Definitions:
#   key  : registry branch itself
#   value: registry item which has a data and type
#   type : type of a value
#   data : data of a value
# Svetaslau Yuntsevich mailto:svetaslauy@checkpoint.com
# Checkpoint Software Technologies Ltd. 2022 (c)
# ======================================================================================================================
from time import sleep
from subprocess import Popen, PIPE, TimeoutExpired


REG_ROOTS = ["HKEY_CLASSES_ROOT", "HKEY_CURRENT_USER", "HKEY_LOCAL_MACHINE", "HKEY_USERS", "HKEY_CURRENT_CONFIG"]


class NoDataExistsException(BaseException):
    """Registry key does not contain any data or does not exist"""
    pass


class NotZeroExitCodeException(BaseException):
    """Command was not executed successful in system call"""
    pass


def __sys_rec(cmd, timeout=None, work_dir=None):
    """Request any command from system"""
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE, cwd=work_dir)
    ret_code = 0
    try:
        proc.communicate(timeout=timeout)
        ret_code = proc.returncode
    except TimeoutExpired:
        ret_code = 5

    return ret_code


def __req(req) -> str:
    """Execute system request and return decoded output"""
    data = None
    proc_ = Popen(req, stdout=PIPE, stderr=PIPE)
    outs, errs = proc_.communicate()
    if proc_.returncode == 0:
        if outs:
            data = outs.decode()
        else:
            raise NoDataExistsException
    else:
        raise NotZeroExitCodeException
    return data


def _root(string) -> bool:
    """REG_ROOTS -> Identify if there is a key in a string"""
    return True if [r for r in REG_ROOTS if r in string] else False


def _value(key) -> list:
    """Work with data and return properties of a value"""

    data_set = list()
    for each_value in _enum(key, recurse=False):
        if each_value:
            if not _root(each_value):
                data_set.append(each_value)

    set_result = list()

    for _ in data_set:
        try:
            set_result.append(_.split()[0])
        except IndexError:
            pass

    return set_result


def _enum(key, recurse=True):
    """
    Iterate over registry branch key
    """
    query = f'reg query "{key}"'
    if recurse:
        query += " /S"
    return __req(query).split('\r\n')[1:-1]


def key_list(key, recurse=True) -> list:
    """
    Get all sub keys from registry by key (registry branch)
    Params:
        key as str() (e.g.: "HKEY_LOCAL_MACHINE\\SYSTEM")
    Returns:
        list of values
    Usage:
        regedit.key_list(key)
    """
    data = list()

    for each_key in _enum(key, recurse):
        if each_key:
            if _root(each_key):
                data.append(each_key)

    return data


def values_list(key) -> list:
    """
    Get list of values for specified key
    Parameters:
        key: key branch to process as str()
    """
    set_result = _value(key)
    return set_result


def value_data(key, value):
    """
    Get value data in specified key
    Parameters:
        key: key branch to process as str()
        value: value name as str()
    Returns:
        value data as str()
    """
    _cmd = r'reg query "{}" /v {}'.format(key, value)

    proc = Popen(_cmd, stdout=PIPE, stderr=PIPE)
    outs, errs = proc.communicate()

    if proc.returncode == 0:
        data = outs.decode().split('\r\n')[2].split('    ')[-1]
        return data
    else:
        return None


def default_value(key=None) -> str:
    """Return default values in key -> no implementation"""
    pass


def del_key(key) -> bool:
    """Delete registry key"""
    query = f'reg delete "{key}" /f'

    error_level = __sys_rec(query)
    return error_level == 0


def del_value(key, value) -> bool:
    """Delete value of a specific key"""
    error_level = __sys_rec(f'reg delete "{key}" /v {value} /F')
    return error_level == 0


def set_value(key, value, data, reg_type=None) -> bool:

    cmd = f'reg add "{key}" /f /v {value} /d {data}'
    if reg_type:
        cmd += f" /t {reg_type}"

    ret_code = __sys_rec(cmd)
    return ret_code == 0


def key_exists(key):
    error_level = __sys_rec(f'reg query "{key}"')
    return error_level == 0


def value_exists(key, value):
    cmd = r'reg query "{}" /v "{}"'.format(key, value)
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    proc.communicate()
    return proc.returncode == 0
