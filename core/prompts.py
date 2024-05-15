import os


class MessageView:

    def __init__(self):
        self.prompt = os.path.join(os.getcwd(), "prompts", "commands")
        self.start = os.path.join(os.getcwd(), "prompts", "start")

    @staticmethod
    def __read(prompt_file):
        with open(prompt_file, "r") as f:
            return f.read()

    def show_commands(self):
        return self.__read(self.prompt)

    def start(self):
        # TODO: TEXT HAS TO BE CONVERTED TO STRING BEFORE <RETURN> OPTION
        return str(self.__read(self.start))

