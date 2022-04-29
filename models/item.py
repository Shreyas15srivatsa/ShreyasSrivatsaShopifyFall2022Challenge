from typing import List
from db import db


class ItemModel(db.Model):
    # create new items table
    __tablename__ = "items"

    # define columns for the items table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    price = db.Column(db.Float(precision=3), nullable=False)
    description = db.Column(db.String(80), nullable=True)
    # warehouse_id indicates which warehouse/location the item belongs to
    warehouse_id = db.Column(
      db.Integer, 
      db.ForeignKey("warehouses.id"), 
      nullable=False
    )
    # define warehouse relationship
    warehouse = db.relationship("WareHouseModel")

    @classmethod
    def find_by_name(cls, name: str) -> "ItemModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["ItemModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
