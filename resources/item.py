
from flask_jwt import jwt_required
from models.item import ItemModel

from flask_restful import Resource, reqparse


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float
                        , required=True,
                        help='this field can not be left blank')

    # data = request.get_json() burada request get json yerine parse arg kullandık
    parser.add_argument('store_id', type=int
                        , required=True,
                        help='every item needs a store_id')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "item is "'{}' " already exist".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured inserting the item.'}, 500  # 500 internal server error anlamında

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'item deleted'}

    def put(self, name):

        data = Item.parser.parse_args()
        # parser kısmını item sınıfnın altına koyduk

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        # connection.commit() burada commite ihtiyacımız yok

        # return {'items': [item.json() for item in ItemModel.query.all()] } alttaki kodla aynı işi yapar alttaki kod javascriptle uygun olabilir
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
