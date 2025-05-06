from py2neo import Graph
from py2neo.ogm import GraphObject
import os
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

def get_graph():
    return Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def init_db():
    graph = get_graph()
    # Create constraints
    graph.run("CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.email IS UNIQUE")
    graph.run("CREATE CONSTRAINT IF NOT EXISTS FOR (p:Post) REQUIRE p.id IS UNIQUE") 