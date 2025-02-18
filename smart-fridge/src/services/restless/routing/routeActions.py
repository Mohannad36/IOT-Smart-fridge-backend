from flask import jsonify
from flask_restful import Resource

class GetWeightSensorById(Resource):
    def get(self):
        return { "Message" : "Hello World!" }

class IsWeightSensorOccupiedById(Resource):
    def get(self):
        return { "Message" : "Hello World Again!" }

class SwaggerJson(Resource):
    def get(self):
        return jsonify({
            "swagger" : "2.0",
            "info" : {
                "title" : "Restless smart-fridge API",
                "version" : "1.0",
                "description" : "Swagger smart-fridge API documentation"
            }})
