import os
import json

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

from models import sqlite, User

from collections.abc import Callable

BASEPATH: str = os.path.abspath(os.path.dirname(__file__))

class restlessApiPlug:
    def __init__(self,
                 applicationPath: str,
                 endpointsConfigPath: str, sqliteDatabaseName: str,
                 newApplication: bool = True, application: Flask = None) -> restlessApiPlug:
        self.application: Flask = application
        if self.application == None:
            self.application = Flask(__name__)

        absoluteApplicationPath: str = "sqlite:///"+os.path.join(applicationPath, "db."+sqliteDatabaseName+".sqlite")
        absoluteEndpointsPath: str = os.path.join(applicationPath, endpointsConfigPath)

        self.application.config["SQLALCHEMY_DATABASE_URI"] = absoluteApplicationPath
        self.application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        sqlite.init_app(self.application)
        with self.application.app_context():
            sqlite.create_all()
        self.manager: Api = Api(self.application)
    def addResource(self,
                    action: Callable, 
                    endpoint: str) -> None:
        if (self.manager == None or action == None or endpoint == None): return
        self.manager.add_resource(action, endpoint)
    def start(self,
              shouldShowDebugInformation = True) -> None:
        if (self.application == None): return
        self.application.run(debug=shouldShowDebugInformation)

class GetWeightSensorById(Resource):
    def get(self):
        return { "Message" : "Hello World!" }

class IsWeightSensorOccupiedById(Resource):
    def get(self):
        return { "Message" : "Hello World Again!" }

def main() -> None: 
    restlessApi: restlessApiPlug = restlessApiPlug(BASEPATH, 
                                                   "endpoints.json", "persistent",
                                                   True, None)
    restlessApi.addResource(GetWeightSensorById, 
                            "/sensor/weight/getById")
    restlessApi.addResource(IsWeightSensorOccupiedById,
                            "/sensor/weight/getOccupiedById")
    restlessApi.start(True)

if __name__ == "__main__":
    main()
