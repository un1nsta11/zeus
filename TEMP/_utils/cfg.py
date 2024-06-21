# ----------------------------------------------------------------------------------------------------------------------
# @author: [Svetaslau Yuntsevich]
# @contact: [svetaslauy@checkpoint.com]
# @project: zang_tests_ng
# @file: cfg.py
# @path: _utils
# @time: 09-Jun-22 16:35
# ----------------------------------------------------------------------------------------------------------------------
import json

__all__ = ['cf', 'data', 'update_json', 'create_json', 'update_data']


def cf(f):
    """Return JSON data from file provided"""
    with open(f, 'r') as jf:
        _data = json.load(jf)
    return _data


def data(file):
    """Return data from JSON file"""
    with open(file, 'r', encoding='utf-8') as f:
        _data = json.load(f)
    return _data


def update_data(file, jdata):
    """Update JSON with data object / create json with data"""
    with open(file, "w", encoding='utf-8') as df:
        json.dump(jdata, df, indent=4)


def update_json(file, key, value):
    """Update JSON file with simple key-value pair"""
    _data = data(file)
    _data[key] = value
    with open(file, "w") as jf:
        json.dump(_data, jf, indent=4)


def create_json(file, _data):
    """Create JSON file with data if it does not exist"""
    with open(file, "w") as ec:
        json.dump(_data, ec, indent=4)
