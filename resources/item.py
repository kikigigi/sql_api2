from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item_model import ItemModel

class Items(Resource):

    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}, 200


class Item(Resource):
    TABLE = 'users'
    parser = reqparse.RequestParser()  # This parser belongs to the class.
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank"
                        )

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id"
                        )

    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_item_by_name(name)
        except:
            return {'message': 'An error occurred while searching for the item.'}, 500
        if item:
            return item.json()
        return {'message': 'Item does not exist.'}, 404

    def post(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            return {"message": f"{name} has already existed"}, 400
        requested_data = Item.parser.parse_args()
        item = ItemModel(name, **requested_data)
        try:
            item.save_to_db() ### change to save_to_db()
        except:
            return {'message': 'An error occurred while inserting data into the database'}, 500
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}, 200
        return {'message': 'Item does not exist'}, 404

    def put(self, name):
        requested_data = Item.parser.parse_args()
        item = ItemModel.find_item_by_name(name)

        if item is None:
            item = ItemModel(name, **requested_data)
        else:
            item.price = requested_data['price']
        item.save_to_db()

        return item.json()