import os
import workspace as workspace

import logging

class logger:
    def __init__(self,
                 logName: str = "default.log", logLevel: str = "INFO") -> None:
        self.log = logging.getLogger(__name__)

        self.level = None
        match logLevel:
            case "INFO":
                self.level = logging.INFO
            case _:
                self.level = logging.INFO 
        self.logConfig = logging.basicConfig(filename=os.path.abspath(os.path.join(os.path.join(workspace.getConfigAttribute("BasePath"), "logging"), logName)), level=self.level)

    def info(self,
             logMessage: str) -> None:
        self.log.info(logMessage)


def setupLogging() -> None:
    basePath: str = workspace.getConfigAttribute("BasePath")
    workspace.setConfigAttribute("logsPath", os.path.abspath(os.path.join(basePath, "logging")))
    if not os.path.exists(workspace.getConfigAttribute("logsPath")):
        os.mkdir(workspace.getConfigAttribute("logsPath"))
