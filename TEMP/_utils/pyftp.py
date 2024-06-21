# ======================================================================================================================
# FTP LIB
# ======================================================================================================================

__all__ = [
    "PyFtp"
]

import logging
import os.path
import shutil
from time import sleep
import ftplib


def _convert_path(path=""):
    return path.replace("\\", "/")


class DownloadFailureException(Exception):
    pass


class PathDoesNotExistsException(Exception):
    pass


class PyFtp:
    """
    Class to work with FTP conveniently
    Supported path format:
        folder/sub_folder/sub_sub_folder
        folder\\sub_folder\\sub_sub_folder
    """

    def __init__(self, address=None, user=None, password=None):
        self.address = address
        self.user = user
        self.password = password
        self.ftp = self._ftp()

    def _ftp(self):
        """Initiate connection"""
        ftp = ftplib.FTP(self.address)
        ftp.login(self.user, self.password)
        return ftp

    def path_exists(self, path='') -> bool:
        """
        Return true if path exists
        :param: path: full path to a file or folder
        Returns:
            True if path exists
            False if path does not exists
        """
        self.ftp.cwd('/')
        path = _convert_path(path)

        _path = path.split('/')
        _path = list(filter(None, _path))

        path_exists = True

        try:
            for _ in _path:
                self.ftp.cwd(_)
        except ftplib.error_perm:
            path_exists = False

        return path_exists

    def dir_list(self, path='') -> list:
        """
        Returns:
             list of items in specified directory
        :param path: full path to directory on ftp
        """
        dir_listing = list()

        self.ftp.cwd('/')

        path = _convert_path(path)
        _path = path.split('/')
        _path = list(filter(None, _path))

        for _ in _path:
            self.ftp.cwd(_)

        try:
            dir_listing = self.ftp.nlst()
        except ftplib.error_perm as resp:
            if str(resp) == "550 No files found":
                pass
            else:
                pass

        return dir_listing

    def isfile(self, path='') -> bool:
        """
        Returns:
             True if path is a file
             False if path is a directory
        :param path: full path on ftp
        """
        self.ftp.cwd('/')
        isfile = True

        path = _convert_path(path)

        if self.path_exists(path):
            try:
                self.ftp.cwd(path)
                isfile = False
            except ftplib.error_perm:
                pass
            return isfile
        else:
            raise FileNotFoundError

    def download_file(self, source, destination) -> None:
        """
        Download single file
        :param source: full path to file with extension
        :param destination: full path to folder where file should be downloaded
        :return: None
        """
        source = _convert_path(source)
        src_file = source.split('/')
        src_file = list(filter(None, src_file))

        try:
            self.ftp.retrbinary("RETR " + source, open(f"{destination}/{src_file[-1]}", 'wb').write)
        except BaseException as err:
            assert err

    def download_content(self, source, destination) -> None:
        """
        Download files content from source directory
        :param source: full path to directory
        :param destination: full path to local directory
        """
        self.ftp.cwd('/')

        source = _convert_path(source)

        content = self.dir_list(source)
        for _ in content:
            if self.isfile(f"{source}/{_}"):
                try:
                    self.ftp.retrbinary("RETR " + f"{source}/{_}", open(f"{destination}/{_}", 'wb').write)
                except BaseException as err:
                    assert err

    def upload_file(self, source, destination="") -> None:
        """
        Method:
            Upload file to ftp
        Parameters:
            :param source: full local path to file
            :param destination: full remote path without file name and extension
            :return: None
        Limitations:
            If source will full path in this function: self.ftp.storbinary(f'STOR "{source}"', f), then upload is not
            possible.
            To solve this problem, copy source file to local path, then upload using try-catch,
            and finally cleanup the file.
        """
        self.ftp.cwd('/')

        destination = _convert_path(destination)
        dst_ = destination.split('/')
        dst_ = list(filter(None, dst_))

        for _ in dst_:
            logging.info(f"Go to {_}")
            self.ftp.cwd(_)
        try:
            # solve limitation:
            shutil.copyfile(source, os.path.basename(source))
            with open(os.path.basename(source), 'rb') as f:
                self.ftp.storbinary(f'STOR {os.path.basename(source)}', f)
        except (PermissionError, OSError, BaseException):
            pass
        finally:
            os.remove(os.path.basename(source))

    def delete(self) -> None:
        """
        Not implemented
        :return: None
        """
        pass

    def mk_tree(self, path="") -> None:
        """
        Make directory tree on ftp
        :param path: path which should be created
        :return: None
        """
        self.ftp.cwd('/')
        path = _convert_path(path)

        _path = path.split('/')
        _path = list(filter(None, _path))

        for _ in _path:
            if _ in self.ftp.nlst():
                self.ftp.cwd(_)
            else:
                self.ftp.mkd(_)
                sleep(3)
                self.ftp.cwd(_)

