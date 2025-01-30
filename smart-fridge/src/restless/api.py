import json

from flask import Flask

class restlessApiPlug:
    def __init__(self, application: Flask) -> any:
        self.application = application

application: Flask = Flask(__name__)
        
@application.route("/", methods=[ "GET" ])
def index() -> str:
    return "<h1>Smart fridge API root . . .</h1>"

@application.route("/sensor/weight/<int:id>", methods=[ "GET" ])
def weightSensor(id) -> str:
    pass
@application.route("/sensor/weight/occupied/<int:id>", methods=[ "GET" ])
def weightSensorOccupied(id) -> str:
    pass

def main() -> None:
    application.run(debug=True)
    api = restlessApiPlug(application)

if __name__ == "__main__":
    main()
