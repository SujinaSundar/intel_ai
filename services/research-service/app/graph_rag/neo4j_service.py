"""
Neo4j connection service.
"""

from neo4j import GraphDatabase

from app.database.config import settings


driver = GraphDatabase.driver(

    settings.NEO4J_URI,

    auth=(

        settings.NEO4J_USERNAME,

        settings.NEO4J_PASSWORD
    )
)


def get_driver():

    """
    Return Neo4j driver.
    """

    return driver