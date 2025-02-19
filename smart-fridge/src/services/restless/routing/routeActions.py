from flask import jsonify
from flask_restful import Resource

class WeightSensorById(Resource):
    def get(self):
        return { "Message" : "Hello World!" }

class IsWeightSensorOccupiedById(Resource):
    def get(self):
        return { "Message" : "Hello World Again!" }

class AllItems(Resource):
    def get(self):
        items = Item.query.all()
        return jsonify([item.serialize() for item in items])

    def post(self):
        data = request.get_json()
        newItem = Item(name=data["name"])

        db.session.add(newItem)
        db.session.commit()
        
        return jsonify(newItem.serialize()), 201

class ItemById(Resource):
    def put(self, itemId):
        item = item.query.get_or_404(itemId)

        data = request.get_json()
        item.name = data["name"]
        db.session.commit()

        return jsonify(item.serialize())

    def delete(self, itemId):
        item = Item.query.get_or_404(itemId)
        
        db.session.delete(item)
        db.session.commit()

        return '', 204

class AllShoppingLists(Resource):
    def get(self):
        lists = ShoppingList.query.all()
        return jsonify([lst.serialize() for lst in lists])

    def post(self):
        data = request.get_json()
        newList = ShoppingList(name=data["name"])

        db.session.add(newList)
        db.session.commit()

        return jsonify(newList.serialize()), 201

class ShoppingListById(Resource):
    def put(self, listId):
        lst = ShoppingList.query.get_or_404(listId)

        data = request.get_json()
        lst.name = data["name"]
        db.session.commit()

        return jsonify(lst.serialize())

    def delete(self, listId):
        lst = ShoppingList.query.get_or_404(listId)

        db.session.delete(lst)
        db.session.commit()

        return '', 204


class SwaggerJson(Resource):
    def get(self):
        return jsonify({
            "swagger" : "2.0",
            "info" : {
                "title" : "Restless smart-fridge API",
                "version" : "1.0",
                "description" : "Swagger smart-fridge API documentation"
            }})
