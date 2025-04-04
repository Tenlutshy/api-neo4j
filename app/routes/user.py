from flask import Blueprint, request, jsonify
from controllers.user_controller import UsersController

users_bp = Blueprint('users', __name__)

@users_bp.route('', methods=['POST'])
def add_user():
    return UsersController.insert(request.get_json())

@users_bp.route('', methods=['GET'])
def get_users():
    return UsersController.get()

@users_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    return UsersController.get_by_id(user_id)

@users_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    return UsersController.update(user_id, request.get_json())

@users_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    return UsersController.delete(user_id)

@users_bp.route('/<user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    return UsersController.get_posts(user_id)

@users_bp.route('/<user_id>/posts', methods=['POST'])
def add_post(user_id):
    return UsersController.insert_post(user_id, request.get_json())


@users_bp.route('/<user_id>/friends', methods=['GET'])
def get_friends(user_id):
    return UsersController.get_friends(user_id)

@users_bp.route('/<user_id>/friends', methods=['POST'])
def add_friend(user_id):
    return UsersController.add_friend(user_id)

@users_bp.route('/<user_id>/friends/<friend_id>', methods=['DELETE'])
def remove_friend(user_id, friend_id):
    return UsersController.remove_friend(user_id, friend_id)

@users_bp.route('/<user_id>/friends/<friend_id>', methods=['GET'])
def are_friends(user_id, friend_id):
    return UsersController.are_friends(user_id, friend_id)

@users_bp.route('/<user_id>/mutual-friends/<other_id>', methods=['GET'])
def mutual_friends(user_id, other_id):
    return UsersController.mutual_friends(user_id, other_id)