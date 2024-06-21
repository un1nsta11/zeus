# ======================================================================================================================
# SMB MANAGER
# Mount and unmount network drives
# ======================================================================================================================
import logging
from subprocess import call
from time import sleep

__all__ = [
    "mount", "unmount"
]


def mount(full_path, local_path='', username=None, password=None, attempts=3) -> bool:
    """
    Mount SMB file share
        :param full_path: full path to SMB file share
        :param local_path: local path where drive should be mounted
        :param username: username
        :param password: password
        :param attempts: retries to mount
    """
    call('net use')

    _mount = f'net use {local_path} {full_path}'
    _mount += f' /user:{username} {password}' if username else False

    mounted = False

    for x in range(attempts):
        error_level = call(_mount, shell=False)
        if error_level == 0:
            mounted = True
            break
        else:
            sleep(5)
            unmount()

    return mounted


def unmount():
    """Unmount all mounted network drives"""
    unmounted = False
    error_level = call(r'net use * /delete /y', shell=False)

    if error_level == 0:
        unmounted = True

    return unmounted
