import importlib
import subprocess
import sys
import os

def stringToClassUsingModule(classNameAsString: str, module: str) -> object:
    if (classNameAsString == None or module == None): return None
    using: object = importlib.import_module(module)
    return getattr(using, classNameAsString)

def runSubprocess(prompt: str) -> any:
  try:
    return subprocess.run(prompt, shell=True, capture_output=True, check=True, encoding="utf-8") \
                     .stdout \
                     .strip()
  except:
    return None

def runSubprocessControlled(args: list, path: str = ".") -> any:
    try:
        return subprocess.Popen(args, shell=True,
                                cwd=path,
                                close_fds=True)
    except:
        return None


def guid() -> str:
  if sys.platform == 'darwin':
    return runSubprocess(
      "ioreg -d2 -c IOPlatformExpertDevice | awk -F\\\" '/IOPlatformUUID/{print $(NF-1)}'",
    )

  if sys.platform == 'win32' or sys.platform == 'cygwin' or sys.platform == 'msys':
    return runSubprocess('wmic csproduct get uuid').split('\n')[2] \
                                         .strip()

  if sys.platform.startswith('linux'):
    return runSubprocess('cat /var/lib/dbus/machine-id') or \
           runSubprocess('cat /etc/machine-id')

  if sys.platform.startswith('openbsd') or sys.platform.startswith('freebsd'):
    return runSubprocess('cat /etc/hostid') or \
           runSubprocess('kenv -q smbios.system.uuid')
