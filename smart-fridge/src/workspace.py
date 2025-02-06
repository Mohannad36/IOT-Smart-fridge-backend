import os
import json

from jsonmerge import merge

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

if __name__ == "__main__":
    main()
