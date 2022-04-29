from typing import List
from db import db


class WareHouseModel(db.Model):
    __tablename__ = "warehouses"

    # define columns for the warehouses table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    # define the relationship b/w warehouses and items
    items = db.relationship("ItemModel", lazy="dynamic", overlaps="warehouse")

    @classmethod
    def find_by_name(cls, name: str) -> "WareHouseModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["WareHouseModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
