from flask_jwt import jwt_required
from models.store import StoreModel

from flask_restful import Resource, reqparse


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.json()

        return {'message': 'store not found'}, 404

    def post(self, name):

        if StoreModel.find_by_name(name):
            return {'message': "store with name '{}' already there!".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'an error occured while creating the store'}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            store.delete_from_db()
            return {'message': 'store deleted'}

        return {'message': 'item can not be found'}


class StoreList(Resource):
    def get(self):
        return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}
