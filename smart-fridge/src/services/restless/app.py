import os
import json

from workspace import *

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

from waitress import serve

from modules.endpointParser import parseEndpoints
from modules.logging import logger

from database.models import db, Fridges 

from collections.abc import Callable

setConfigAttribute("RestlessBasePath", os.path.abspath(os.path.dirname(__file__)))
setConfigAttribute("RestlessRoutePath", os.path.abspath(os.path.join(getConfigAttribute("RestlessBasePath"), "routing")))

log: logger = logger("restless-service.log", "INFO")

class restlessApiPlug:
    def __init__(self,
                 databasePath: str,
                 endpointsConfigPath: str, 
                 sqliteDatabaseName: str,
                 newApplication: bool = True, application: Flask = None) -> None:
        self.application: Flask = application
        if self.application == None:
            self.application = Flask(__name__)

        setConfigAttribute("RestlessDatabasePath", os.path.abspath(os.path.join(os.path.join(getConfigAttribute("RestlessBasePath"), databasePath), "data")))
        setConfigAttribute("RestlessDatabaseFilePath", "sqlite:///"+os.path.abspath(os.path.join(getConfigAttribute("RestlessDatabasePath"), "db."+sqliteDatabaseName+".sqlite")))
        setConfigAttribute("RestlessEndpointsConfigPath", os.path.abspath(os.path.join(getConfigAttribute("RestlessBasePath"), endpointsConfigPath)))

        if not os.path.exists(getConfigAttribute("RestlessDatabasePath")):
            os.makedirs(getConfigAttribute("RestlessDatabasePath"))

        self.application.config["SQLALCHEMY_DATABASE_URI"] = getConfigAttribute("RestlessDatabaseFilePath")
        self.application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        db.init_app(self.application)
        with self.application.app_context():
            db.create_all()
        self.manager: Api = Api(self.application)
    def loadResource(self,
                    action: Callable, 
                    endpoint: str) -> None:
        if (self.manager == None or action == None or endpoint == None): return
        self.manager.add_resource(action, endpoint)
    def dynamicLoadResources(self) -> None:
        endpoints: dict = parseEndpoints(getConfigAttribute("RestlessEndpointsConfigPath"))
        for endpointUrl, endpointAction in endpoints.items():
            if endpointAction == None: continue
            self.loadResource(endpointAction, endpointUrl)
    def start(self,
              shouldShowDebugInformation = True) -> None:
        if (self.application == None): return
        serve(self.application, host="0.0.0.0", port=5000)

def main() -> None:
    log.info("Started")
    restlessApi: restlessApiPlug = restlessApiPlug(".",
                                                   "routing/endpoints.json", 
                                                   "persistent",
                                                   True, None)
    restlessApi.dynamicLoadResources()
    restlessApi.start(True)
    log.info("Finished")

if __name__ == "__main__":
    main()
