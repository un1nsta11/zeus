import os
from time import sleep
import logging

from _utils import proc, tsch


class NodeControl:
    """
    Control connection between node and jenkins server
    """

    def __init__(self):
        self.agent_root_process = "java.exe"
        self.agent_logs_root = "C:\\jenkins\\remoting\\logs"
        self.agent_tasks = ["jenkins_agent", "jenkins_watchdog"]
        self.connected_patt = "INFO: Connected"

    def disconnect_node(self):
        """
        Disconnect node from jenkins
        """
        logging.info("Disconnect node from jenkins server")
        proc.stop_proc(self.agent_root_process)
        [tsch.end(_) for _ in self.agent_tasks]
        [tsch.disable(_) for _ in self.agent_tasks]

    def connect_node(self):
        """
        Start and stop jenkins agent to disconnect the node
        """
        attempts = 5
        while attempts != 0:
            if not self._connected():
                logging.info(f"Connect node to Jenkins server. Run agent, attempts remains: {attempts}")
                self.disconnect_node()
                sleep(5)
                tsch.enable(self.agent_tasks[0])
                tsch.run(self.agent_tasks[0])
                sleep(60)
                attempts -= 1
            else:
                logging.info("Node connected successful")
                break

        tsch.enable(self.agent_tasks[1])
        tsch.run(self.agent_tasks[1])

        sleep(5)
        return True

    def _connected(self) -> bool:
        self.__cleanup()
        connected = False

        try:
            with open(os.path.join(self.agent_logs_root, "remoting.log.0"), "r") as agent_:
                _data = agent_.readlines()

            if _data:
                for _line in _data:
                    if self.connected_patt in _line:
                        connected = True
                        break
        except FileNotFoundError:
            pass

        return connected

    def __cleanup(self):
        try:
            for _ in os.listdir(self.agent_logs_root):
                _path = os.path.join(self.agent_logs_root, _)
                os.remove(_path) if os.path.exists(_path) else None
        except PermissionError:
            pass


if __name__ == '__main__':
    NodeControl().connect_node()
