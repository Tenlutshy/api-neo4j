from flask import request, jsonify
from models.user_model import User
from models.post_model import Post
from db import graph, matcher
from py2neo import Relationship

class UsersController:
    @staticmethod
    def get():
        users = graph.run("MATCH (u:User) RETURN u").data()
        return jsonify([u['u'] for u in users])

    @staticmethod
    def get_by_id(id):
        user = matcher.match("User", id=id).first()
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        return jsonify(dict(user))
    
    @staticmethod
    def get_posts(id):
        query = """
        MATCH (u:User {id: $user_id})-[:CREATED]->(p:Post)
        RETURN p
        """
        posts = graph.run(query, user_id=id).data()
        return jsonify([p['p'] for p in posts])
    
    @staticmethod
    def update(id, data):
        user = matcher.match("User", id=id).first()
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        user['name'] = data.get('name', user['name'])
        user['email'] = data.get('email', user['email'])
        graph.push(user)
        return jsonify(dict(user))
    
    @staticmethod
    def delete(id):
        user = matcher.match("User", id=id).first()
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        graph.delete(user)
        return jsonify({'message': 'Utilisateur supprimé'})
    
    @staticmethod
    def insert(data):
        user = User(data['name'], data['email'])
        user.save()
        return jsonify(user.to_dict()), 201
    
    @staticmethod
    def insert_post(user_id, data):
        title = data.get('title')
        content = data.get('content')

        post = Post(title, content)
        post.save()
        post.link_creator(user_id)

        return jsonify(post.to_dict()), 201
    
    def get_friends(user_id):
        query = """
        MATCH (u:User {id: $user_id})-[:FRIENDS_WITH]-(f:User)
        RETURN f
        """
        friends = graph.run(query, user_id=user_id).data()
        return jsonify([f['f'] for f in friends])

    def add_friend(user_id):
        data = request.get_json()
        friend_id = data.get('friend_id')
        u1 = matcher.match("User", id=user_id).first()
        u2 = matcher.match("User", id=friend_id).first()
        if not u1 or not u2:
            return jsonify({'error': 'Utilisateur ou ami introuvable'}), 404
        graph.create(Relationship(u1, "FRIENDS_WITH", u2))
        return jsonify({'message': 'Amitié ajoutée'})

    def remove_friend(user_id, friend_id):
        query = """
        MATCH (u1:User {id: $user_id})-[r:FRIENDS_WITH]-(u2:User {id: $friend_id})
        DELETE r
        """
        graph.run(query, user_id=user_id, friend_id=friend_id)
        return jsonify({'message': 'Amitié supprimée'})

    def are_friends(user_id, friend_id):
        query = """
        MATCH (u1:User {id: $user_id})-[:FRIENDS_WITH]-(u2:User {id: $friend_id})
        RETURN u1, u2
        """
        result = graph.run(query, user_id=user_id, friend_id=friend_id).data()
        return jsonify({'friends': len(result) > 0})

    def mutual_friends(user_id, other_id):
        query = """
        MATCH (a:User {id: $user_id})-[:FRIENDS_WITH]-(f:User)-[:FRIENDS_WITH]-(b:User {id: $other_id})
        RETURN f
        """
        mutuals = graph.run(query, user_id=user_id, other_id=other_id).data()
        return jsonify([f['f'] for f in mutuals])