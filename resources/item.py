from http import HTTPStatus
from flask_restful import Resource
from flask import request
from models.item import ItemModel
from schemas.item import ItemSchema
from constants import Items

# load the item and item list schemas
item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)

class Item(Resource):
  
    @classmethod
    def get(cls, name: str):
        item = ItemModel.find_by_name(name)
        # if the inventory item is found, return it else throw 404
        if item:
            return item_schema.dump(item), HTTPStatus.OK

        return {"message": Items.ITEM_NOT_FOUND}, HTTPStatus.NOT_FOUND

    @classmethod
    def post(cls, name: str):
        # if inventory item already exist, throw 400
        if ItemModel.find_by_name(name):
            return {"message": Items.NAME_ALREADY_EXISTS.format(name)}, HTTPStatus.BAD_REQUEST

        item_json = request.get_json()
        item_json["name"] = name

        item = item_schema.load(item_json)

        try:
            item.save_to_db()
        except:
            return {"message": Items.ERROR_INSERTING}, HTTPStatus.INTERNAL_SERVER_ERROR

        return item_schema.dump(item), HTTPStatus.CREATED

    @classmethod
    def delete(cls, name: str):
        # get inventory item, and if present, try to delete
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": Items.ITEM_DELETED}, HTTPStatus.OK

        return {"message": Items.ITEM_NOT_FOUND}, HTTPStatus.NOT_FOUND

    @classmethod
    def put(cls, name: str):
        item_json = request.get_json()
        item = ItemModel.find_by_name(name)

        # if inventory item already exists, update the price and
        # descriiption fields from the put request body
        # else, create a new item and add to the db
        if item:
            item.price = item_json["price"]
            item.description = item_json["description"]
        else:
            item_json["name"] = name
            item = item_schema.load(item_json)

        item.save_to_db()

        return item_schema.dump(item), HTTPStatus.OK


class ItemList(Resource):
    @classmethod
    def get(cls):
        return {"items": item_list_schema.dump(ItemModel.find_all())}, HTTPStatus.OK
