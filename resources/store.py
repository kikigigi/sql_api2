from flask_restful import Resource
from flask_jwt import jwt_required
from models.store_model import StoreModel


class Stores(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}


class Store(Resource):
    @jwt_required()
    def get(self, name):
        store = StoreModel.find_store_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_store_by_name(name):
            return {"message": f"{name} has already existed"}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred while inserting data into the database'}, 500
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_store_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': 'Store deleted'}

