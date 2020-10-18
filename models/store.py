import sqlite3
from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel',
                            lazy='dynamic')  # lazy parametresini verdiğimizde aradaki ilişkiyi json fonksiyonunu çağırdığımızda kurmasıdır

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(
            name=name).first()  # SELECT * FROM ITEMS WHERE name = name ile aynı işi yapıyor , id 1 yaprak ilk sonucu al dediks

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
