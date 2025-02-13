import os
import workspace as workspace

from modules.utils import runSubprocessControlled

def setupCaching():
    basePath: str = workspace.getConfigAttribute("BasePath")
    workspace.setConfigAttribute("cacheFilePath", os.path.abspath(os.path.join(basePath, ".cache")))
    if not os.path.exists(workspace.getConfigAttribute("cacheFilePath")):
        cacheFile = open(workspace.getConfigAttribute("cacheFilePath"), "w+")
        cacheFile.close()

def runSubprocessControlledCached(prompt: str) -> any:
    try:
        newProcess: any = runSubprocessControlled(prompt, workspace.getConfigAttribute("BasePath"))
        newProcessPid: int = newProcess.pid
        print(f"[+] New Subprocess Start With Pid: {newProcessPid} . . .")
        return newProcess
    except subprocess.CalledProcessError as error:
        print(f"[-] New Subprocess Start Error: {error} . . .")
        return None
