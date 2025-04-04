
from flask import Blueprint
from controllers.post_controller import PostsController

posts_bp = Blueprint('posts', __name__)

@posts_bp.route('', methods=['GET'])
def get_posts():
    return PostsController.get()

@posts_bp.route('/<post_id>', methods=['GET'])
def get_post(post_id):
    return PostsController.get_by_id(post_id)


@posts_bp.route('/<post_id>', methods=['PUT'])
def update_post(post_id):
    return PostsController.update(post_id)

@posts_bp.route('/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    return PostsController.delete(post_id)

@posts_bp.route('/<post_id>/comments', methods=['POST'])
def add_comment(post_id):
    return PostsController.insert_comment(post_id)

@posts_bp.route('/<post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    return PostsController.get_comments(post_id)

@posts_bp.route('/<post_id>/like', methods=['POST'])
def like_post(post_id):
    return PostsController.insert_like(post_id)

@posts_bp.route('/<post_id>/like', methods=['DELETE'])
def unlike_post(post_id):
    return PostsController.delete_like(post_id)