import configparser
from py2neo import Graph, NodeMatcher
from time import sleep

config = configparser.ConfigParser()
config.read(".conf")

uri = config.get("database", "uri")
user = config.get("database", "user")
password = config.get("database", "password")

for _ in range(10):
    try:
        graph = Graph(uri, auth=(user, password))
        matcher = NodeMatcher(graph)

        break
    except Exception as e:
        print("⏳ En attente de Neo4j...", str(e))
        sleep(2)
else:
    raise ConnectionError("❌ Impossible de se connecter à Neo4j après plusieurs tentatives.")
