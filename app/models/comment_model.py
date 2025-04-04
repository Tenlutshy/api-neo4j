import time
import uuid
from db import graph
from py2neo import Relationship

from models.base_model import BaseModel
from models.user_model import User
from models.post_model import Post

def timestamp():
    return int(time.time())

class Comment(BaseModel):
    def __init__(self, content):
        super().__init__("Comment", id=str(uuid.uuid4()), content=content, created_at=timestamp())

    def link_to_post_and_user(self, user_id, post_id):
        user = User.get_by_id("User", user_id)
        post = Post.get_by_id("Post", post_id)

        if user and post:
            graph.create(Relationship(user, "CREATED", self.node))
            graph.create(Relationship(post, "HAS_COMMENT", self.node))