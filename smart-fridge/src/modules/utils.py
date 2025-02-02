import importlib

def stringToClassUsingModule(classNameAsString: str, module: str) -> object:
    if (classNameAsString == None or module == None): return None
    using: object = importlib.import_module(module)
    return getattr(using, classNameAsString)
