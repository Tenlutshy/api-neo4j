import time
import uuid

from models.base_model import BaseModel

def timestamp():
    return int(time.time())

class User(BaseModel):
    def __init__(self, name, email):
        super().__init__("User", id=str(uuid.uuid4()), name=name, email=email, created_at=timestamp())