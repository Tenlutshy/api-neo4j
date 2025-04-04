from flask import request, jsonify
from models.comment_model import Comment
from db import graph, matcher
from py2neo import Relationship

class PostsController:
    @staticmethod
    def get():
        posts = graph.run("MATCH (p:Post) RETURN p").data()
        return jsonify([p['p'] for p in posts])

    @staticmethod
    def get_by_id(id):
        post = matcher.match("Post", id=id).first()
        if not post:
            return jsonify({'error': 'Post non trouvé'}), 404
        return jsonify(dict(post))
    
    @staticmethod
    def get_comments(post_id):
        query = """
        MATCH (p:Post {id: $post_id})-[:HAS_COMMENT]->(c:Comment)
        RETURN c
        """
        comments = graph.run(query, post_id=post_id).data()
        return jsonify([c['c'] for c in comments])

    @staticmethod
    def update(id):
        data = request.get_json()
        post = matcher.match("Post", id=id).first()
        if not post:
            return jsonify({'error': 'Post non trouvé'}), 404
        post['title'] = data.get('title', post['title'])
        post['content'] = data.get('content', post['content'])
        graph.push(post)
        return jsonify(dict(post))

    @staticmethod
    def delete(id):
        post = matcher.match("Post", id=id).first()
        if not post:
            return jsonify({'error': 'Post non trouvé'}), 404
        graph.delete(post)
        return jsonify({'message': 'Post supprimé'})
    
    @staticmethod
    def insert_comment(post_id):
        data = request.get_json()
        user_id = data.get('user_id')
        content = data.get('content')
        
        comment = Comment(content)
        comment.save()
        comment.link_to_post_and_user(user_id, post_id)
        return jsonify(comment.to_dict()), 201
    
    @staticmethod
    def insert_like(post_id):
        data = request.get_json()
        user_id = data.get('user_id')
        
        user = matcher.match("User", id=user_id).first()
        post = matcher.match("Post", id=post_id).first()
        
        if not user or not post:
            return jsonify({'error': 'Utilisateur ou post introuvable'}), 404
        
        graph.create(Relationship(user, "LIKES", post))
        return jsonify({'message': 'Like ajouté'}), 201
    
    @staticmethod
    def delete_like(post_id):
        data = request.get_json()
        user_id = data.get('user_id')
        
        query = """
        MATCH (u:User {id: $user_id})-[l:LIKES]->(p:Post {id: $post_id})
        DELETE l
        """
        graph.run(query, user_id=user_id, post_id=post_id)
        return jsonify({'message': 'Like supprimé'})