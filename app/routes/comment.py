from flask import Blueprint
from controllers.comment_controller import CommentsController

comments_bp = Blueprint('comments', __name__)

@comments_bp.route('', methods=['GET'])
def get_comments():
    return CommentsController.get()

@comments_bp.route('/<comment_id>', methods=['GET'])
def get_comment(comment_id):
    return CommentsController.get_by_id(comment_id)

@comments_bp.route('/<comment_id>', methods=['PUT'])
def update_comment(comment_id):
    return CommentsController.update(comment_id)

@comments_bp.route('/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    return CommentsController.delete(comment_id)

@comments_bp.route('/<comment_id>/like', methods=['POST'])
def like_comment(comment_id):
    return CommentsController.insert_like(comment_id)

@comments_bp.route('/<comment_id>/like', methods=['DELETE'])
def unlike_comment(comment_id):
    return CommentsController.delete_like(comment_id)




