import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str
                        , required=True,
                        help='this field can not be left blank')
    parser.add_argument('password', type=str
                        , required=True,
                        help='this field can not be left blank')

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'this username already taken'}, 400

        new_user = UserModel(
            **data)  # data içeriğini yukarda kendimiz belirttiğimiz için çift yıldız burada şu anlama geliyor = data['username'],data['passwword']

        new_user.save_to_db()

        return {'message': 'user created succesfully'}, 201
