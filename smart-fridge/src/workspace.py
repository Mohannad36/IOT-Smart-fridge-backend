import os
import json
import psutil
import shlex
import signal

from jsonmerge import merge

from modules.utils import guid
from modules.cache import *
from modules.logging import *

class Workspace:
    config = { "BasePath" : os.path.dirname(os.path.abspath(__file__)) }
    def __getitem__(self, indice):
        pass
    def __setitem__(self, indice, data):
        pass
    def __str__(self):
        stringRepresentation = ""
        for key, value in self.config.items():
            stringRepresentation += "(" + key + "::" + value + ") "
        return stringRepresentation

def getConfigAttribute(attribute):
    if not os.path.exists(".env"):
        newEnvironmentFile = open(".env", "w+")
        newEnvironmentFile.close()
    if os.path.getsize(".env") > 0:
        with open (".env", "r") as paths:
            Workspace.config = json.load(paths)
    return Workspace.config[attribute]

def setConfigAttribute(attribute, value):
    if not os.path.exists(".env"):
        newEnvironmentFile = open(".env", "w+")
        newEnvironmentFile.close()

    Workspace.config[attribute] = value
    currentJsonConfig: str = None
    newPathsAsJson: str = json.dumps(Workspace.config)

    if os.path.getsize(".env") > 0:
        with open (".env", "r") as paths:
            currentJsonConfig = json.load(paths)
    with open (".env", "w+") as paths:
        paths.write(merge(currentJsonConfig, newPathsAsJson))

def main() -> None:
    if not os.path.exists(".env"):
        newEnvironmentFile = open(".env", "w+") 
    setConfigAttribute("GUID", guid())

    setupCaching()
    setupLogging()

    restlessServiceProcess: any = None
    receiverServiceProcess: any = None
    screenServiceProcess: any = None

    savedServicePidLines: list = []

    if os.path.getsize(getConfigAttribute("cacheFilePath")) > 0:
        with open(getConfigAttribute("cacheFilePath"), "r") as cache:
            for servicePidLine in cache:
                if len(servicePidLine) == 0 or servicePidLine == "\n": 
                    continue

                serviceName, pid = servicePidLine.split(":")
                pid = int(pid)

                if psutil.pid_exists(pid):
                    match serviceName:
                        case "restless":
                            restlessServiceProcess = psutil.Process(pid)
                            print("NO START RESTLESS")
                        case "receiver":
                            receiverServiceProcess = psutil.Process(pid)
                            print("NO START RECEIVER")
                        case "screen":
                            screenServiceProcess = psutil.Process(pid)
                            print("NO START SCREEN")
                    savedServicePidLines.append(servicePidLine)
    with open(getConfigAttribute("cacheFilePath"), "w+") as cache:
        if not restlessServiceProcess:
            restlessServiceProcess = runSubprocessControlledCached(shlex.split("poetry run restless-service"))
            print("START RESTLESS")
            cache.write(f"restless:{restlessServiceProcess.pid}\n")
        if not receiverServiceProcess:
            receiverServiceProcess = runSubprocessControlledCached(shlex.split("poetry run receiver-service"))
            print("START RECEIVER")
            cache.write(f"receiver:{receiverServiceProcess.pid}\n")
        if not screenServiceProcess:
            screenServiceProcess = runSubprocessControlledCached(shlex.split("poetry run screen-service"))
            print("START SCREEN")
            cache.write(f"screen:{screenServiceProcess.pid}\n")
        for savedServicePidLine in savedServicePidLines:
            cache.write(savedServicePidLine+"\n")


if __name__ == "__main__":
    main()
