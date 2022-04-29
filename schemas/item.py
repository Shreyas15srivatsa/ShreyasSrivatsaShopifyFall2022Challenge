from ma import ma
from models.item import ItemModel
from models.warehouse import WareHouseModel

class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModel
        load_only = ("warehouse",)
        dump_only = ("id",)
        include_fk = True
        load_instance = True