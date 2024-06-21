#!/usr/bin/env python3
import json
import os
import logging
from logging import config
from threading import Thread

from core.utils.execmd import Cmder

logging.config.fileConfig(os.path.join(os.getcwd(), 'config', 'logconf.ini'))
logging = logging.getLogger('zeus')


class TaskScheduler:

    def __init__(self):
        self.tasks = os.path.join(os.getcwd(), "config", "tasks.json")

    def __read(self):
        if not os.path.exists(self.tasks):
            logging.error("Tasks file not found! Exiting from task scheduler")
            return None

        with open(self.tasks, "r") as json_tasks:
            data = json.load(json_tasks)
        return data

    def run(self):
        tasklist = self.__read()

        if tasklist is None:
            logging.error("TaskScheduler cannot find tasks file! Exiting!")
            return False

        for task_name, task_data in tasklist.items():
            logging.debug(f"Task: {task_name}; Data: {task_data}")
            logging.info(f"Task: {task_name}, command: {task_data['cmd']}, uptime: {task_data['uptime']}, "
                         f"execution directory: {task_data['workdir']}")
            Thread(
                target=Cmder(command=task_data['cmd'],
                             workdir=task_data['workdir'],
                             uptime=task_data['uptime']).exec_cmd,
                args=(), name=task_name).start()

