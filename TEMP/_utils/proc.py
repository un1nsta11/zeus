# ======================================================================================================================
# PROCESS LIB
# Dependencies: psutil
# ======================================================================================================================
import logging
import os
from subprocess import PIPE, Popen
import psutil


__all__ = [
    "process_up", "processes_up", "processes_down", "processes_pid", "down_instances", "up_instances", "stop_proc",
    "pid_used", "stop_by_pid", "proc_exists"
]


def __proc_exists(pname):
    """Validate if process exists or not"""
    for proc in psutil.process_iter():
        try:
            if pname.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def __procs_property(proc_name) -> list:
    """Internal -> Get property of a process"""
    props = list()
    for proc in psutil.process_iter():
        try:
            pdata = proc.as_dict(attrs=['pid', 'name', 'create_time', 'status', 'memory_percent'])
            if proc_name.lower() in pdata['name'].lower():
                props.append(pdata)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return props


def proc_exists(pname):
    return __proc_exists(pname)


def process_up(proc_name) -> bool:
    """Return True if process is running else False"""
    running = False
    try:
        for proc in psutil.process_iter():
            if proc.name() == proc_name:
                if proc.status() != 'stopped':
                    running = True
    except psutil.NoSuchProcess:
        pass

    return running


def processes_up(proc_list) -> list:
    """Returns list of processes which are running"""
    up_procs = list()
    for proc in proc_list:
        if process_up(proc):
            logging.info(f"Process running: {proc}")
            up_procs.append(proc)

    return up_procs


def processes_down(proc_list) -> list:
    """Returns processes list if they are not running"""
    down_procs = list()
    for proc in proc_list:
        if not process_up(proc):
            logging.info(f"Process not running: {proc}")
            down_procs.append(proc)

    return down_procs


def processes_pid(proc_name) -> list:
    """Returns processes PID`s in list"""
    pid_list = list()

    for _ in __procs_property(proc_name):
        pid_list.append(_['pid'])

    return pid_list


def down_instances(proc_name=str()) -> int:
    """Get num of process instances which are down"""
    inst_down = 0

    for _ in __procs_property(proc_name):
        if _['status'] == 'stopped':
            inst_down += 1

    return inst_down


def up_instances(proc_name=str()) -> int:
    """Returns num of running instances if a specific process"""
    inst_up = 0

    for _ in __procs_property(proc_name):
        if _['status'] != 'stopped':
            inst_up += 1

    return inst_up


def stop_proc(proc_name):
    """Terminate process by process name"""
    if __proc_exists(proc_name):
        # proc = Popen(f'TASKKILL /F /IM {proc_name}', stdout=PIPE, stderr=PIPE)
        # error_level = proc.returncode
        error_level = os.system(f'TASKKILL /F /IM {proc_name}')
        return error_level == 0
    else:
        return False


def stop_by_pid(proc_pid):
    """Terminate process by PID"""
    proc = Popen(f'TASKKILL /F /PID {proc_pid}', stdout=PIPE, stderr=PIPE)
    error_level = proc.returncode
    return error_level == 0


def pid_used(pid):
    """Return True if process pid is already is used"""
    return psutil.pid_exists(pid)


def proc_props(pid):
    """Get process property by process PID"""
    "Get-WmiObject -Query 'Select CommandLine FROM ' "
    pass