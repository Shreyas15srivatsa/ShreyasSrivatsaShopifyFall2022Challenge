from http import HTTPStatus
from flask_restful import Resource
from models.warehouse import WareHouseModel
from schemas.warehouse import WareHouseSchema
from constants import WareHouses

# load the warehouse schemas
warehouse_schema = WareHouseSchema()
warehouse_list_schema = WareHouseSchema(many=True)


class WareHouse(Resource):
    @classmethod
    def get(cls, name: str):
        warehouse = WareHouseModel.find_by_name(name)
        print(warehouse)
        if warehouse:
            return warehouse_schema.dump(warehouse), HTTPStatus.OK
          
        return {
          "message": WareHouses.WAREHOUSE_NOT_FOUND.value
        }, HTTPStatus.NOT_FOUND

    @classmethod
    def post(cls, name: str):
        if WareHouseModel.find_by_name(name):
            return {
              "message": WareHouses.NAME_ALREADY_EXISTS.value.format(name)
            }, HTTPStatus.BAD_REQUEST

        warehouse = WareHouseModel(name=name)
        try:
            warehouse.save_to_db()
        except:
            return {
              "message": WareHouses.ERROR_INSERTING.value
            }, HTTPStatus.INTERNAL_SERVER_ERROR

        return warehouse_schema.dump(warehouse), HTTPStatus.CREATED

    @classmethod
    def delete(cls, name: str):
        warehouse = WareHouseModel.find_by_name(name)
        if warehouse:
            # convert warehouse obj to json
            warehouse_json = warehouse_schema.dump(warehouse)
            # if the warehouse has items in it's inventory, we cannot
            # delete the warehouse before emptying the inventory
            if len(warehouse_json["items"]):
              return {
                "message": WareHouses.WAREHOUSE_INVENTORY_NOT_EMPTY.value
              }, HTTPStatus.BAD_REQUEST
              
            warehouse.delete_from_db()
          
            return {
              "message": WareHouses.WAREHOUSE_DELETED.value
            }, HTTPStatus.OK

        return {
          "message": WareHouses.WAREHOUSE_NOT_FOUND.value
        }, HTTPStatus.NOT_FOUND


class WareHouseList(Resource):
    @classmethod
    def get(cls):
        return {
          "warehouses": warehouse_list_schema.dump(WareHouseModel.find_all())
        }, HTTPStatus.OK
