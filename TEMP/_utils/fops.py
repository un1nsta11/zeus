
__all__ = [
    "version", "file_hash", "wait_for_file", "wait_for_line_in_file", "wait_for_directory_removed"
]

import logging
from time import sleep
import os
from subprocess import Popen, PIPE
from hashlib import sha1, md5, sha256


def __sys_req(query):
    data = None
    proc_ = Popen(query, stdout=PIPE, stderr=PIPE)
    outs, errs = proc_.communicate()
    if proc_.returncode == 0:
        if outs:
            data = outs.decode()
        else:
            pass
    else:
        raise BaseException
    return data


def version(file_path) -> str:
    """Get version of a file"""
    return __sys_req(f'powershell (Get-Item "{file_path}" ).VersionInfo.FileVersion').replace(",", ".").strip()


def file_hash(filepath, hash_type='md5') -> str:
    """Get file hash"""
    if hash_type == 'md5':
        hash_func = md5()
    elif hash_type == 'sha1':
        hash_func = sha1()
    elif hash_type == 'sha256':
        hash_func = sha256()
    else:
        raise Exception('Unknown hash type! Available parameters: md5, sha1, sha256.')
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)

    return str(hash_func.hexdigest())


def wait_for_file(filename, timeout, period) -> bool:
    """
    Loop for waiting for specific path.
    :param filename: full path to file
    :param timeout: full time to wait in sec
    :param period: delay between file check
    :return: True if file exists; exit by timeout else
    """
    time_passed = 0
    exists = False
    while True:
        if time_passed >= timeout:
            logging.info(f'Wait for file exit by timeout: {timeout}. {filename}')
            break

        if os.path.exists(filename):
            logging.info(f'File detected: {filename}. Exit loop')
            exists = True
            break
        else:
            sleep(period)
            time_passed += period
            continue

    return exists


def wait_for_directory_removed(folder_path: str, timeout=300, period=60) -> bool:
    time_passed = 0
    exists = True
    while True:
        if time_passed >= timeout:
            logging.info(f'Wait for folder removed exit by timeout: {timeout}. {folder_path}')
            break

        if not os.path.exists(folder_path):
            logging.info(f'Folder disparaged: {folder_path}. Exit loop')
            exists = False
            break
        else:
            sleep(period)
            time_passed += period
            continue

    return exists


def wait_for_line_in_file(filename, entry, timeout, period=0.1):
    """
    Wait for specific line in file
    :param filename: full path to file
    :param entry: entry to find in each line
    :param timeout: max wait time
    :param period: time to wait between file checks
    :return: True if found match; otherwise false
    """
    file = open(filename, 'r')
    found_match = False
    logging.info(f'Wait for "{entry}" in "{filename}"')
    try:
        time_passed = 0
        while True:
            if time_passed > timeout:
                logging.info(f'. Wait for line in "{filename}". Exit by timeout')
                break
            line = file.readline()
            if line:
                if entry.lower() in line.lower():
                    logging.info(f'Found match. "{entry}" in "{line}"')
                    found_match = True
                    break
            else:
                time_passed += period
                sleep(period)
    finally:
        file.close()

    return found_match
