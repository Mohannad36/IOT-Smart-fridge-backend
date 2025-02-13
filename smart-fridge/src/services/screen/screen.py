import time

from modules.logging import logger

log: logger = logger("screen-service.log", "INFO")

class screenPlug:
    def __init__(self) -> any:
        pass

def main() -> None:
    log.info("Started")
    screen = screenPlug()
    while True:
        time.sleep(1)
    log.info("Finished")

if __name__ == "__main__":
    main()
