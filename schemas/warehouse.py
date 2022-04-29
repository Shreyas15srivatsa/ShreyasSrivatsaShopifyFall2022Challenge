from ma import ma
from models.warehouse import WareHouseModel
from models.item import ItemModel
from schemas.item import ItemSchema

class WareHouseSchema(ma.SQLAlchemyAutoSchema):
    items = ma.Nested(ItemSchema, many=True)

    class Meta:
        model = WareHouseModel
        dump_only = ("id",)
        include_fk = True
        load_instance = True