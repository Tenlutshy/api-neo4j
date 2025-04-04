from py2neo import Node
from db import graph, matcher

class BaseModel:
    def __init__(self, label, **properties):
        self.label = label
        self.node = Node(label, **properties)

    def save(self):
        """Crée le nœud dans Neo4j."""
        graph.create(self.node)

    def to_dict(self):
        """Convertit le nœud en dictionnaire."""
        return dict(self.node)

    @classmethod
    def get_by_id(cls, label, node_id):
        """Récupère un nœud par son ID et label."""
        return matcher.match(label, id=node_id).first()

    @classmethod
    def delete_by_id(cls, label, node_id):
        """Supprime un nœud par son ID et label."""
        node = cls.get_by_id(label, node_id)
        if node:
            graph.delete(node)
            return True
        return False

    @classmethod
    def exists(cls, label, node_id):
        """Vérifie l'existence d'un nœud."""
        return cls.get_by_id(label, node_id) is not None
