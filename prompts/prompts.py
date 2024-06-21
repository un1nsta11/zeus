import os
import logging
import json

from logging import config

logging.config.fileConfig(os.path.join(os.getcwd(), 'config', 'logconf.ini'))
logging = logging.getLogger('zeus')


class Prompts(object):
    PROMPTS = os.path.join(os.getcwd(), "prompts", "db.json")
    START = "start"
    HELP = "help"
    COMMANDS = "commands"


class Prompt:

    def __init__(self, prompt_type):
        self.prompt = Prompts.PROMPTS
        self.prompt_type = prompt_type


    def _read(self):
        if not os.path.exists(self.prompt):
            logging.error("Fatal error occurred: prompts file not found.")
            exit(1)
        with open(self.prompt, "r") as f:
            data = json.load(f)
        return data

    def show(self) -> str:
        return "".join(self._read().get(self.prompt_type))

