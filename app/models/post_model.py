import time
import uuid
from models.user_model import User
from models.base_model import BaseModel
from py2neo import Relationship
from db import graph

def timestamp():
    return int(time.time())

class Post(BaseModel):
    def __init__(self, title, content):
        super().__init__("Post", id=str(uuid.uuid4()), title=title, content=content, created_at=timestamp())

    def link_creator(self, user_id):
        user = User.get_by_id("User", user_id)
        if user:
            graph.create(Relationship(user, "CREATED", self.node))