# ----------------------------------------------------------------------------------------------------------------------
# @author: [Svetaslau Yuntsevich]
# @contact: [svetaslauy@checkpoint.com]
# @project: zone_alarm
# @file: zip.py
# @path: _utils
# @time: 22-Feb-23 13:58
# ----------------------------------------------------------------------------------------------------------------------
from os.path import expandvars as ev
from os import remove
from zipfile import ZipFile


__all__ = ["unzip"]


def unzip(zip_path: str, dest_folder: str, del_zip=True) -> None:
    with ZipFile(ev(zip_path), "r") as zip_file:
        zip_file.extractall(path=ev(dest_folder))
        zip_file.close()
    __delete_original(zip_path) if del_zip else None


def zipf():
    raise NotImplementedError


def __delete_original(zip_path):
    remove(ev(zip_path))
