import os
import json
import time

import psutil
import shlex
import signal

from dotenv import set_key, load_dotenv

from modules.utils import guid
from modules.cache import *
from modules.logger import *

set_key(".env", "BasePath", os.path.dirname(os.path.abspath(__file__)))

def identifyRunningServices() -> None:
    restlessServiceProcess: any = None
    receiverServiceProcess: any = None
    screenServiceProcess: any = None
    proxyServiceProcess: any = None

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
                            print("[/] RESTLESS SERVICE ALREADY RUNNING . . .")
                        case "receiver":
                            receiverServiceProcess = psutil.Process(pid)
                            print("[/] RECEIVER SERVICE ALREADY RUNNING . . .")
                        case "screen":
                            screenServiceProcess = psutil.Process(pid)
                            print("[/] SCREEN SERVICE ALREADY RUNNING . . .")
                        case "proxy":
                            proxyServiceProcess = psutil.Process(pid)
                            print("[/] PROXY SERVICE ALREADY RUNNING . . .")
                    savedServicePidLines.append(servicePidLine)
    with open(getConfigAttribute("cacheFilePath"), "w+") as cache:
        if not restlessServiceProcess:
            restlessServiceProcess = runSubprocessControlledCached(shlex.split("poetry run restless-service"))
            print("[+] STARTING RESTLESS SERVICE . . .")
            cache.write(f"restless:{restlessServiceProcess.pid}\n")
        time.sleep(2)

        if not receiverServiceProcess:
            receiverServiceProcess = runSubprocessControlledCached(shlex.split("poetry run receiver-service"))
            print("[+] STARTING RECEIVER SERVICE . . .")
            cache.write(f"receiver:{receiverServiceProcess.pid}\n")
        time.sleep(2)

        if not screenServiceProcess:
            screenServiceProcess = runSubprocessControlledCached(shlex.split("poetry run screen-service"))
            print("[+] STARTING SCREEN SERVICE . . .")
            cache.write(f"screen:{screenServiceProcess.pid}\n")
        time.sleep(2)

        if not proxyServiceProcess:
            proxyServiceProcess = runSubprocessControlledCached(shlex.split("poetry run proxy-service"))
            print("[+] STARTING PROXY SERVICE . . .")
            cache.write(f"proxy:{proxyServiceProcess.pid}\n")

        for savedServicePidLine in savedServicePidLines:
            cache.write(savedServicePidLine+"\n")

def getConfigAttribute(attribute):
    if not os.path.exists(".env"):
        newEnvironmentFile = open(".env", "w+")
        newEnvironmentFile.close()
    load_dotenv(".env")
    return os.getenv(attribute)

def setConfigAttribute(attribute, value):
    if not os.path.exists(".env"):
        newEnvironmentFile = open(".env", "w+")
        newEnvironmentFile.close()
    set_key(".env", attribute, value)

def main() -> None:
    import database.manipulate as sql

    setConfigAttribute("GUID", guid())

    setupCaching()
    setupLogging()

    sql.insertNewFridgeIfNotExists()

    while True:
        identifyRunningServices()
        time.sleep(30)

if __name__ == "__main__":
    main()
