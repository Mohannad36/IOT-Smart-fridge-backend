import os
import json

import importlib

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

from endpointParser import parseEndpoints

from database.models import sqlite, User

from collections.abc import Callable

BASEPATH: str = os.path.abspath(os.path.dirname(__file__))

class restlessApiPlug:
    def __init__(self,
                 applicationPath: str,
                 endpointsConfigPath: str, sqliteDatabaseName: str,
                 newApplication: bool = True, application: Flask = None) -> None:
        self.application: Flask = application
        if self.application == None:
            self.application = Flask(__name__)

        dataDirectory: str = os.path.join(applicationPath, "data")
        if not os.path.exists(dataDirectory):
            os.makedirs(dataDirectory)

        self.absoluteApplicationPath: str = "sqlite:///"+os.path.join(dataDirectory, "db."+sqliteDatabaseName+".sqlite")
        self.absoluteEndpointsPath: str = os.path.join(applicationPath, endpointsConfigPath)

        self.application.config["SQLALCHEMY_DATABASE_URI"] = self.absoluteApplicationPath
        self.application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        sqlite.init_app(self.application)
        with self.application.app_context():
            sqlite.create_all()
        self.manager: Api = Api(self.application)
    def loadResource(self,
                    action: Callable, 
                    endpoint: str) -> None:
        if (self.manager == None or action == None or endpoint == None): return
        self.manager.add_resource(action, endpoint)
    def dynamicLoadResources(self) -> None:
        endpoints: dict = parseEndpoints(self.absoluteEndpointsPath)
        for endpointUrl, endpointAction in endpoints.items():
            if endpointAction == None: continue
            self.loadResource(endpointAction, endpointUrl)
    def start(self,
              shouldShowDebugInformation = True) -> None:
        if (self.application == None): return
        self.application.run(debug=shouldShowDebugInformation)

def main() -> None: 
    restlessApi: restlessApiPlug = restlessApiPlug(BASEPATH, 
                                                   "routing/endpoints.json", "persistent",
                                                   True, None)
    restlessApi.dynamicLoadResources()
    restlessApi.start(True)

if __name__ == "__main__":
    main()
