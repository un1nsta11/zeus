# ----------------------------------------------------------------------------------------------------------------------
# @author: [Svetaslau Yuntsevich]
# @contact: [svetaslauy@checkpoint.com]
# @project: zone_alarm
# @file: db.py
# @path: _utils
# @time: 05-Apr-23 11:45
# @readme: Add system variables before using:
#   - SETX FRAMEWORK_DATABASE "path_to_db" && SETX -m FRAMEWORK_DATABASE "path_to_db"
# ----------------------------------------------------------------------------------------------------------------------
import json

from os.path import expandvars as ev

__all__ = ["add", "query", "upd", "rm"]
__version__ = 1.0

DATABASE = ev("%FRAMEWORK_DATABASE%")


def add(key: str, sub_key: str, value: str, data: str):
    with open(DATABASE, "r") as database:
        pass


def query(key: str, sub_key: str, value: str, data: str):
    pass


def upd(key: str, sub_key: str, value: str, data: str):
    pass


def rm(key: str, sub_key: str, value: str, data: str):
    pass
