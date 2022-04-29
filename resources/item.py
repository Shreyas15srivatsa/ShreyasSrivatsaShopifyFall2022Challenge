from http import HTTPStatus
from flask_restful import Resource
from flask import request
from models.item import ItemModel
from models.warehouse import WareHouseModel
from schemas.item import ItemSchema
from schemas.warehouse import WareHouseSchema
from constants import Items

# load the schemas
item_schema = ItemSchema()
warehouse_list_schema = WareHouseSchema(many=True)
item_list_schema = ItemSchema(many=True)

class Item(Resource):
  
    @classmethod
    def get(cls, name: str):
        item = ItemModel.find_by_name(name)
        # if the inventory item is found, return it else throw 404
        if item:
            return item_schema.dump(item), HTTPStatus.OK

        return {
          "message": Items.ITEM_NOT_FOUND.value
        }, HTTPStatus.NOT_FOUND

    @classmethod
    def post(cls, name: str):
        # if inventory item already exist, throw 400
        if ItemModel.find_by_name(name):
            return {
              "message": Items.NAME_ALREADY_EXISTS.value.format(name)
            }, HTTPStatus.BAD_REQUEST

        item_json = request.get_json()
      
        warehouse_id = item_json["warehouse_id"]
        # verify if the warehouse_id provided in the 
        # request is valid
        is_valid = Item.verify_warehouse_id(warehouse_id)
        if len(is_valid):
          return is_valid, HTTPStatus.BAD_REQUEST
          
        item_json["name"] = name

        item = item_schema.load(item_json)

        try:
            item.save_to_db()
        except:
            return {
              "message": Items.ERROR_INSERTING.value
            }, HTTPStatus.INTERNAL_SERVER_ERROR

        return item_schema.dump(item), HTTPStatus.CREATED

    @classmethod
    def delete(cls, name: str):
        # get inventory item, and if present, try to delete
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {
              "message": Items.ITEM_DELETED.value
            }, HTTPStatus.OK

        return {
          "message": Items.ITEM_NOT_FOUND.value
        }, HTTPStatus.NOT_FOUND

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
          
            warehouse_id = item_json["warehouse_id"]
            # verify if the warehouse_id provided in the 
            # update request is valid
            is_valid = Item.verify_warehouse_id(warehouse_id)
            if len(is_valid):
              return is_valid, HTTPStatus.BAD_REQUEST

            item.warehouse_id = warehouse_id
        else:
            item_json["name"] = name
            item = item_schema.load(item_json)

        item.save_to_db()

        return item_schema.dump(item), HTTPStatus.OK

    @staticmethod
    def verify_warehouse_id(warehouse_id: int) -> dict:
      """
      Helper method that verifies if the provided warehouse_id is valid
      Get the warehouse_id specified in the request and 
      build a list of valid warehouse ids to check
      if the warehouse id provided is valid
      """
      all_warehouses = warehouse_list_schema.dump(
        WareHouseModel.find_all()
      )
      valid_ids = []
      for warehouse in all_warehouses:
        valid_ids.append(warehouse["id"])
        
      if warehouse_id not in valid_ids:
        return {
          "message": Items.INVALID_WAREHOUSE.value
        }
      else:
        return {}


class ItemList(Resource):
    @classmethod
    def get(cls):
        return {
          "items": item_list_schema.dump(ItemModel.find_all())
        }, HTTPStatus.OK
