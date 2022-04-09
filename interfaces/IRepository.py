""" File that contains the abstract class of a repository
"""
from abc import ABC, abstractmethod


class IRepository(ABC):
    """ Abstract class that defines the methods every repository must have.
    """
    @abstractmethod
    def __init__(self):
        """ Method that inits the repositry object. """

    @abstractmethod
    def insert_one(self, element):
        """ Method to insert one element to database.

        Args:
            element: Pydantic object to be inserted to database
        """

    @abstractmethod
    def insert_many(self, elements):
        """ Method to insert multiple elements to database.

        Args:
            elements: List of pydantic objects to be inserted to database
        """

    @abstractmethod
    def find_one(self, _filter, projection):
        """ Method to get one element from database.

        Args:
            _filter: Criteria to filter and find one element
            projection: Fields to be returned or not from the found element
        """

    @abstractmethod
    def find_many(self, _filter, projection, sort, currentPage, pageSize):
        """ Method to get multiple elements from database.

        Args:
            _filter: Criteria to filter and find multiple elements
            projection: Fields to be returned or not from the found elements
            sort: Determines the sort field and direction of the results
            currentPage: Field used for pagination. Specifies a specific set
                         of results to be returned.
            pageSize: Field used for pagination. Determines the number of
                      elements that will be returned.
        """

    @abstractmethod
    def delete_one(self, _filter):
        """ Method that deletes one element from database.

        Args:
            _filter: Criteria to filter the document that will be deleted
        """

    @abstractmethod
    def update_one(self, _filter, update):
        """ Method that updates an existing element in database.

        Args:
            _filter: Criteria to filter the document that will be updated
            update: Fields and values that will be updated
        """
