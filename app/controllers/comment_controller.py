from flask import request, jsonify
from models.comment_model import Comment
from db import graph, matcher
from py2neo import Relationship

class CommentsController:
    @staticmethod
    def get():
        comments = graph.run("MATCH (c:Comment) RETURN c").data()
        return jsonify([c['c'] for c in comments])

    @staticmethod
    def get_by_id(id):
        comment = matcher.match("Comment", id=id).first()
        if not comment:
            return jsonify({'error': 'Commentaire non trouvé'}), 404
        return jsonify(dict(comment)), 200

    @staticmethod
    def update(id):
        data = request.get_json()
        comment = matcher.match("Comment", id=id).first()
        if not comment:
            return jsonify({'error': 'Commentaire non trouvé'}), 404
        comment['content'] = data.get('content', comment['content'])
        graph.push(comment)
        return jsonify(dict(comment)), 200

    @staticmethod
    def delete(id):
        comment = matcher.match("Comment", id=id).first()
        if not comment:
            return jsonify({'error': 'Commentaire non trouvé'}), 404
        graph.delete(comment)
        return jsonify({'message': 'Commentaire supprimé'}), 200
    
    @staticmethod
    def insert_like(comment_id):
        data = request.get_json()
        user_id = data.get('user_id')
        
        user = matcher.match("User", id=user_id).first()
        comment = matcher.match("Comment", id=comment_id).first()
        
        if not user or not comment:
            return jsonify({'error': 'Utilisateur ou post introuvable'}), 404
        
        graph.create(Relationship(user, "LIKES", comment))
        return jsonify({'message': 'Like ajouté'}), 201
    
    @staticmethod
    def delete_like(comment_id):
        data = request.get_json()
        user_id = data.get('user_id')
        query = """
        MATCH (u:User {id: $user_id})-[l:LIKES]->(c:Comment {id: $comment_id})
        DELETE l
        """
        graph.run(query, user_id=user_id, comment_id=comment_id)
        return jsonify({'message': 'Like supprimé'})