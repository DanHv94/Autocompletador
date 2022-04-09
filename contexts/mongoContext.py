""" File that creates a database connection with MongoDB and yields a
connection object as a singleton.
"""
from pymongo import MongoClient

from config import MONGO_URI
from models.singleton import Singleton


class MongoConnection(metaclass=Singleton):
    """ Class that creates the connection with Mongo DB """
    def __init__(self):
        client = MongoClient(MONGO_URI)
        self.db = client.get_database()


def get_mongo():
    """ Creates a MongoConnection instance and returns it.

    This function is inteded to be used with Fast API Depends to inject
    the connection as a dependency.

    Returns:
        db: Mongo Database
    """
    mongo = MongoConnection()
    yield mongo.db