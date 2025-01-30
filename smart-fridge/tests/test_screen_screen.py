from src.screen.screen import screenPlug

def test_initialize() -> None:
    screen: screenPlug = screenPlug()
    assert screen != None
