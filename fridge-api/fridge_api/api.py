import json

from flask import Flask

app: Flask = Flask(__name__)

@app.route("/", methods=[ "GET" ])
def index() -> str:
    return "<h1>Smart fridge API root . . .</h1>"

@app.route("/sensor/weight/<int:id>", methods=[ "GET" ])
def weightSensor(id) -> str:
    pass
@app.route("/sensor/weight/occupied/<int:id>", methods=[ "GET" ])
def weightSensorOccupied(id) -> str:
    pass

def main() -> None:
    app.run(debug=True)

if __name__ == "__main__":
    main()