import os
import json

from workspace import workspace

import importlib

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

from modules.endpointParser import parseEndpoints

from database.models import sqlite, User

from collections.abc import Callable

workspace["RestlessBasePath"] = os.path.abspath(os.path.dirname(__file__))
workspace["RestlessRoutePath"] = os.path.abspath(os.path.join(workspace["RestlessBasePath"], "routing"))

class restlessApiPlug:
    def __init__(self,
                 databasePath: str,
                 endpointsConfigPath: str, 
                 sqliteDatabaseName: str,
                 newApplication: bool = True, application: Flask = None) -> None:
        self.application: Flask = application
        if self.application == None:
            self.application = Flask(__name__)

        workspace["RestlessDatabasePath"] = os.path.abspath(os.path.join(os.path.join(workspace["RestlessBasePath"], databasePath), "data"))
        workspace["RestlessDatabaseFilePath"] = "sqlite:///"+os.path.abspath(os.path.join(workspace["RestlessDatabasePath"], "db."+sqliteDatabaseName+".sqlite"))
        workspace["RestlessEndpointsConfigPath"] = os.path.abspath(os.path.join(workspace["RestlessBasePath"], endpointsConfigPath))

        if not os.path.exists(workspace["RestlessDatabasePath"]):
            os.makedirs(workspace["RestlessDatabasePath"])

        self.application.config["SQLALCHEMY_DATABASE_URI"] = workspace["RestlessDatabaseFilePath"]
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
        endpoints: dict = parseEndpoints(workspace["RestlessEndpointsConfigPath"])
        for endpointUrl, endpointAction in endpoints.items():
            if endpointAction == None: continue
            self.loadResource(endpointAction, endpointUrl)
    def start(self,
              shouldShowDebugInformation = True) -> None:
        if (self.application == None): return
        self.application.run(debug=shouldShowDebugInformation)

def main() -> None: 
    restlessApi: restlessApiPlug = restlessApiPlug(".",
                                                   "routing/endpoints.json", 
                                                   "persistent",
                                                   True, None)
    restlessApi.dynamicLoadResources()
    restlessApi.start(True)

if __name__ == "__main__":
    main()
