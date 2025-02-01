import os
import json

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

from models import sqlite, User

from collections.abc import Callable

BasePath: str = os.path.abspath(os.path.dirname(__file__))

class restlessApiPlug:
    def __init__(self, application: Flask) -> any:
        self.application = application

        sqlite.init_app(application)
        with application.app_context():
            sqlite.create_all()
        self.manager: Api = Api(self.application)
    def addResource(self,
                    action: Callable, 
                    endpoint: str):
        if (self.manager == None or action == None or endpoint == None): return
        self.manager.add_resource(action, endpoint)

application: Flask = Flask(__name__)
application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BasePath, "db.persistent.sqlite")
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

class GetWeightSensorById(Resource):
    def get(self):
        return { "Message" : "Hello World!" }

class IsWeightSensorOccupiedById(Resource):
    def get(self):
        return { "Message" : "Hello World Again!" }

def main() -> None: 
    restlessApi: restlessApiPlug = restlessApiPlug(application)
    restlessApi.addResource(GetWeightSensorById, 
                            "/sensor/weight/getById")
    restlessApi.addResource(IsWeightSensorOccupiedById,
                            "/sensor/weight/getOccupiedById")
    application.run(debug=True)

if __name__ == "__main__":
    main()
