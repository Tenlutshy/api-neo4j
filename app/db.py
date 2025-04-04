import configparser
from py2neo import Graph, NodeMatcher

config = configparser.ConfigParser()
config.read("../.conf")

uri = config.get("database", "uri")
user = config.get("database", "user")
password = config.get("database", "password")

print(uri, user, password)

graph = Graph(uri, auth=(user, password))
matcher = NodeMatcher(graph)