# ======================================================================================================================
# SERVICE LIB
# Dependencies: psutil
# ======================================================================================================================
import os
import logging

from time import sleep
from subprocess import PIPE, Popen, TimeoutExpired, STDOUT

__all__ = [
    "as_dict", "stop_service", "start_service", "service_up", "can_shutdown", "can_pause", "can_stop", "set_startup",
    "services_up",
    "services_down", "set_disable"
]


def __sys_exec(command, timeout=None, work_dir=None) -> int:
    """
    Execute command and return exit code
    :param command: command <- str()
    :param timeout: seconds <- int()
    :param work_dir: path <- str()
    :return: error_level <- int()
    """
    proc = Popen(command, stdout=PIPE, stderr=PIPE, cwd=work_dir)
    try:
        proc.communicate(timeout=timeout)
        error_level = proc.returncode
    except TimeoutExpired:
        return 5
    return error_level


def __ps_exec(cmd):
    output = Popen(cmd, stderr=STDOUT, stdout=PIPE)
    output_collected = output.communicate()[0], output.returncode
    command_out = output_collected[0].decode('utf-8').strip()
    return command_out


def __ps_bool(cmd):
    if 'False' in __ps_exec(cmd):
        return False
    elif 'True' in __ps_exec(cmd):
        return True


def __status(cmd):
    if 'Running' in __ps_exec(cmd):
        return True
    elif 'Stopped' in __ps_exec(cmd):
        return False


def __sc_query(service):
    """Return service running using sc query command"""

    sc_query = Popen(f'sc query {service}', stdout=PIPE, stderr=PIPE)
    outs, errs = sc_query.communicate()
    output = outs.decode()

    if errs:
        return errs.decode()

    if 'RUNNING' in output:
        running = True
    elif 'FAILED' in output or 'STOPPED' in output:
        running = False
    else:
        running = None

    return running


# ====================================
# Perform an action on service
# ====================================


def stop_service(service_name) -> bool:
    """
    Desc:
        Terminate Service
    Returns:
        True if success else False
    """
    return __sys_exec(f"powershell Stop-Service -Name {service_name} -Force", timeout=180) == 0


def stop_driver(driver_name) -> int:
    error_level = __sys_exec(f"powershell Stop-Service -Name {driver_name} -Force", timeout=180)
    return error_level


def start_service(service_name) -> bool:
    """Start Service"""
    return os.system(f"powershell Start-Service -Name {service_name}") == 0


# ====================================
# Query service statuses
# ====================================


def wait_service_up(driver, timeout, period):
    logging.info(f"Driver {driver} is not RUNNING. Starting waiting for RUNNING state.")
    time_passed = 0
    running = False
    while True:
        if time_passed >= timeout:
            logging.info(f'Wait for driver is RUNNING exit by timeout: {timeout}. {driver}')
            break

        if service_up(driver):
            logging.info(f'Driver is RUNNING: {driver}. Exit loop')
            running = True
            break
        else:
            sleep(period)
            time_passed += period
            continue

    return running


def service_up(service) -> bool:
    """Return is service running"""
    return __sc_query(service) is True


def services_down(svc_list):
    """Returns list of services which are not running"""
    down_list = list()
    for svc in svc_list:
        if __sc_query(svc) is False:
            down_list.append(svc)

    return down_list


def services_up(svc_list):
    """Returns list of services which are running"""
    up_list = list()
    for svc in svc_list:
        if __sc_query(svc) is True:
            up_list.append(svc)

    return up_list


# ====================================
# Query service props
# ====================================


def can_shutdown(service) -> bool:
    """Get property for a service: CanShutDown"""
    return __ps_bool(f"powershell Get-Service -Name {service} | Select-Object -ExpandProperty CanStop")


def can_pause(service) -> bool:
    """Get property for a service: CanPauseAndContinue"""
    return __ps_bool(f"powershell Get-Service -Name {service} | Select-Object -ExpandProperty CanPauseAndContinue")


def can_stop(service) -> bool:
    """Get property for a service: CanStop"""
    return __ps_bool(f"powershell Get-Service -Name {service} | Select-Object -ExpandProperty CanStop")


# ====================================
# Set service statuses
# ====================================


def set_startup(service, manual=True) -> bool:
    """Change service startup type"""
    if manual:
        type_ = "Manual"
    else:
        type_ = "Automatic"

    return os.system(f"powershell Set-Service -Name {service} -StartupType {type_}") == 0


def set_disable(service) -> bool:
    """Change service startup type to Disabled"""
    return os.system(f"powershell Set-Service -Name {service} -StartupType Disabled") == 0


def as_dict(service, try_stop=False, set_manual=False, set_disabled=False) -> dict:
    """
    Return service info as dictionary
    """
    data = dict()
    data['running'] = __sc_query(service) is True
    data['can_shutdown'] = can_shutdown(service)
    data['can_stop'] = can_stop(service)
    data['can_pause'] = can_pause(service)

    data['set_manual'] = set_startup(service) if set_manual else None
    data['set_disabled'] = set_disable(service) if set_disabled else None
    data['set_stop'] = stop_service(service) if try_stop else None

    return data
