from flask import request
from flask_restful import Resource

from models.user import UserModel
from schemas.user import UserSchema
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
from blacklist import BLACKLIST

user_schema = UserSchema()

# constants
USER_NOT_FOUND = "{} not found"
USER_ALREADY_EXISTS = "{} already exists"
USER_CREATED = "User: {} created successfully"
USER_DELETED = "User: {} deleted successfully"
INVALID_PASSWORD = "Invalid Password"
USER_LOGGED_OUT = "User logged out successfully"


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user = user_schema.load(request.get_json())

        if UserModel.find_user_by_email(user.email):
            return {"msg": USER_ALREADY_EXISTS.format(user.email)}, 400

        user.save_to_db()
        return {"msg": USER_CREATED.format(user.email)}, 201


class User(Resource):
    @classmethod
    @jwt_required
    def get(cls, mobile_number):  # get using phone number (can be changed per use case)
        user = UserModel.find_user_by_mobile_number(mobile_number=mobile_number)
        if not user:
            return {"msg": USER_NOT_FOUND.format(mobile_number)}, 404
        return user_schema.dump(user), 200

    # just for testing
    @classmethod
    def delete(cls, mobile_number):
        user = UserModel.find_user_by_mobile_number(mobile_number=mobile_number)
        if not user:
            return {"msg": USER_NOT_FOUND.format(mobile_number)}, 404

        user.delete_from_db()
        return {"msg": USER_DELETED.format(user.email)}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_data = user_schema.load(request.get_json(), partial=("full_name", "mobile_number"))

        user = UserModel.find_user_by_email(email=user_data.email)
        if not user:
            return {"msg": USER_NOT_FOUND.format(user_data.email)}, 401
        elif user.password != user_data.password:
            return {"msg": INVALID_PASSWORD}, 401

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)
        return {"access_token": access_token, "refresh_token": refresh_token}, 200


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]
        BLACKLIST.add(jti)
        return {"msg": USER_LOGGED_OUT}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=user_id, fresh=True)  # creating new fresh token
        return {"access_token": new_access_token}, 200
