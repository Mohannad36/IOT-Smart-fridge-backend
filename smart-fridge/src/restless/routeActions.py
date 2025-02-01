from flask_restful import Resource

class GetWeightSensorById(Resource):
    def get(self):
        return { "Message" : "Hello World!" }

class IsWeightSensorOccupiedById(Resource):
    def get(self):
        return { "Message" : "Hello World Again!" }
