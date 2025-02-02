import os

class BaseWorkspace:
    def __getitem__(self, indice):
        return config[indice]
    def __setitem__(self, indice, data):
        config[indice] = data;

global config
config = {
        "BasePath" : os.path.dirname(__file__),
}

global workspace
workspace = BaseWorkspace()

def main() -> None:
    pass

if __name__ == "__main__":
    main()
