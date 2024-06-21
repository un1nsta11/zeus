# ======================================================================================================================
# TASK SCHEDULER LIB
# ======================================================================================================================
import os
from subprocess import Popen, PIPE, TimeoutExpired
from xml.etree import ElementTree as ET


__all__ = [
    "exists", "create", "run", "end", "disable", "enable"
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
    error_level = 0
    try:
        proc.communicate(timeout=timeout)
        error_level = proc.returncode
    except TimeoutExpired:
        error_level = 5
    return error_level


def exists(task) -> bool:
    """Check if task exists in scheduler by name"""
    return __sys_exec(f'SCHTASKS /Query /TN {task}') == 0


def create(task, cmd, args='', work_dir='', privileges=True, on_boot=False) -> bool:
    """
    Desc:
        Create task in task scheduler
    Note:
        on_boot is bool which set settings into the task that it must be launched only after reboot
        Notice, that after this task will be launched -> it should be deleted by something or someone.
    """
    scheme = r"http://schemas.microsoft.com/windows/2004/02/mit/task"
    root_elem = ET.Element('Task', attrib={"xmlns": f"{scheme}", 'version': "1.2"})

    if on_boot:
        triggers = ET.SubElement(root_elem, 'Triggers')
        logon_trigger = ET.SubElement(triggers, 'LogonTrigger')
        logon_trigger_on = ET.SubElement(logon_trigger, 'Enabled')
        logon_trigger_on.text = "true"

    actions = ET.SubElement(root_elem, 'Actions', attrib={'Context': "Author"})

    exec_ = ET.SubElement(actions, 'Exec')
    command = ET.SubElement(exec_, 'Command')
    command.text = cmd
    if args:
        args_ = ET.SubElement(exec_, 'Arguments')
        args_.text = args

    if work_dir:
        work_dir_ = ET.SubElement(exec_, 'WorkingDirectory')
        work_dir_.text = work_dir

    principals = ET.SubElement(root_elem, 'Principals')
    principal = ET.SubElement(principals, 'Principal', attrib={'id': 'Author'})

    if privileges:
        run_level = ET.SubElement(principal, 'RunLevel')
        run_level.text = 'HighestAvailable'
    et = ET.ElementTree(root_elem)

    xml_filename = os.path.abspath('{}.xml'.format(task))
    et.write(xml_filename, xml_declaration=True, encoding="utf-16")

    return __sys_exec(f'SCHTASKS /Create /TN "{task}" /XML {xml_filename} /F') == 0


def run(task) -> bool:
    """Start task in task scheduler"""
    return __sys_exec(f'SCHTASKS /Run /TN "{task}"') == 0


def end(task) -> bool:
    """End task in task scheduler"""
    return __sys_exec(f'SCHTASKS /End /TN "{task}"') == 0


def disable(task) -> bool:
    """Disable task"""
    return __sys_exec(f'SCHTASKS /Change /TN "{task}" /Disable') == 0


def enable(task) -> bool:
    """Enable task"""
    return __sys_exec(f'SCHTASKS /Change /TN "{task}" /Enable') == 0
