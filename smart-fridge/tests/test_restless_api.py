from src.restless.api import restlessApiPlug 

def test_initialize() -> None:
    api: restlessApiPlug = restlessApiPlug(None)
    assert api != None
