from flask import jsonify
from flask_restful import Resource

from database.models import Items, ShoppingLists

import database.manipulate as sql

class WeightSensorById(Resource):
    def get(self):
        return { "Message" : "Hello World!" }

class IsWeightSensorOccupiedById(Resource):
    def get(self):
        return { "Message" : "Hello World Again!" }

class AllItems(Resource):
    def get(self):
        items = sql.queryAllItems()
        return jsonify([item.serialize() for item in items])

    def post(self):
        data = request.get_json()
        newItem = Items(name=data["name"])

        db.session.add(newItem)
        db.session.commit()
        
        return jsonify(newItem.serialize()), 201

class ItemById(Resource):
    def put(self, itemId):
        item = sql.queryItem(itemId)

        data = request.get_json()
        item.name = data["name"]
        db.session.commit()

        return jsonify(item.serialize())

    def delete(self, itemId):
        item = sql.queryItem(itemId)
        
        db.session.delete(item)
        db.session.commit()

        return '', 204

class AllShoppingLists(Resource):
    def get(self):
        lists = sql.queryAllShoppingLists()
        return jsonify([lst.serialize() for lst in lists])

    def post(self):
        data = request.get_json()
        newList = ShoppingLists(name=data["name"])

        db.session.add(newList)
        db.session.commit()

        return jsonify(newList.serialize()), 201

class ShoppingListById(Resource):
    def put(self, listId):
        lst = sql.queryShoppingList(listId)

        data = request.get_json()
        lst.name = data["name"]
        db.session.commit()

        return jsonify(lst.serialize())

    def delete(self, listId):
        lst = sql.queryShoppingList(listId)

        db.session.delete(lst)
        db.session.commit()

        return '', 204


class SwaggerJson(Resource):
    def get(self):
        return jsonify(
        {
            "swagger": "2.0",
            "info": 
            {
                "title": "Restless smart-fridge API",
                "version": "1.0",
                "description": "Swagger smart-fridge API documentation"
            },
            "paths": 
            {
                "/sensor/weight": 
                {
                    "get": 
                    {
                        "summary": "Get all weight sensor values currently stored in the database",
                        "description": "Returns a list of JSON string of weight sensor values",
                        "responses": 
                        {
                            "200": 
                            {
                                "description": "Success",
                                "schema": 
                                {
                                    "type": "array",
                                    "items": 
                                    {
                                        "type": "object",
                                        "properties": 
                                        {
                                            "guid": { "type": "string" },
                                            "value": { "type": "float" }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "/sensor/weight/getById": 
                {
                    "get": 
                    {
                        "summary": "Get specific weight sensor value from database",
                        "description": "Returns a JSON string of the weight sensor value",
                        "responses": 
                        {
                            "200": 
                            {
                                "description": "Success",
                                "schema": 
                                {
                                    "type": "object",
                                    "properties": 
                                    {
                                        "guid": { "type": "string" },
                                        "value": { "type": "float" }
                                    }
                                }
                            }
                        }
                    }
                },
                "/sensor/weight/getOccupiedById": 
                {
                    "get": 
                    {
                        "summary": "Get occupied status value of specific sensor from database",
                        "description": "Returns a JSON string of the weight sensors occupied status",
                        "responses": 
                        {
                            "200": 
                            {
                                "description": "Success",
                                "schema": 
                                {
                                    "type": "object",
                                    "properties": 
                                    {
                                        "guid": { "type": "string" },
                                        "occupied": { "type": "boolean" }
                                    }
                                }
                            }
                        }
                    }
                },
                "/items": 
                {
                    "get": 
                    {
                        "summary": "Get all items currently stored in the database",
                        "description": "Returns a list of JSON string of items",
                        "responses": 
                        {
                            "200": 
                            {
                                "description": "Success",
                                "schema": 
                                {
                                    "type": "array",
                                    "items": 
                                    {
                                        "type": "object",
                                        "properties": 
                                        {
                                            "name": { "type": "string" },
                                            "quantity": { "type": "integer" },
                                            "expiration": { "type": "string" }
                                        }
                                    }
                                }
                            }
                        }   
                    }
                },
                "/items/getItemById": 
                {
                    "get": 
                    {
                        "summary": "Get a item currently stored in the database",
                        "description": "Returns a JSON string of the item",
                        "responses": 
                        {
                            "200": 
                            {
                                "description": "Success",
                                "schema": 
                                {
                                    "type": "object",
                                    "properties": 
                                    {
                                        "name": { "type": "string" },
                                        "quantity": { "type": "integer" },
                                        "expiration": { "type": "string" },
                                        "partOfShoppingListWithId": { "type": "integer" }
                                    }
                                }
                            }
                        }
                    }
                },
                "/shoppingLists": 
                {
                    "get": 
                    {
                        "summary": "Get all shopping lists currently stored in the database",
                        "description": "Returns a list of JSON string of shopping lists",
                        "responses": 
                        {
                            "200": 
                            {
                                "description": "Success",
                                "schema": 
                                {
                                    "type": "array",
                                    "items": 
                                    { 
                                        "type": "object",
                                        "properties": 
                                        {
                                            "name": { "type": "string" },
                                            "created": { "type": "string" }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "/shoppingLists/getShoppingListById": 
                {
                    "get": 
                    {
                        "summary": "Get a shopping list currently stored in the database",
                        "description": "Returns a JSON string of a shopping list",
                        "responses": 
                        {
                            "200": 
                            {
                                "description": "Success",
                                "schema": 
                                {
                                    "type": "object",
                                    "properties": 
                                    {
                                        "name": { "type": "string" },
                                        "created": { "type": "string" }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        })
