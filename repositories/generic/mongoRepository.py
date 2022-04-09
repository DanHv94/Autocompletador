""" File that contains the definition of the MongoRepository class.
This class is the base class of all repositories and implements the
IRepository interface to connect to mongo.

Attributes:
    logger(logging.Logger): Configured logger object
"""
import logging
from typing import List, Union

from bson.objectid import ObjectId
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError, WriteError

from interfaces.IRepository import IRepository
from models.pydantic import MongoModel


logger = logging.getLogger(__name__)


class MongoRepository(IRepository):
    """ Generic class to implement database logic for mongo. This agnostic
    class implements CRUD at database level.

    Instance Attributes:
        __collection(Collection): Mongo collection
        model(UserMongo): Mongo database model
        __activity(Collection): Activity collection to register inserts,
                                updates and deletes
    """
    def __init__(self) -> None:
        """ Inits all necessary attributes for the MongoRepository object.
        """
        super().__init__()
        self.__collection: Collection = None
        self.model: MongoModel = None

    def set_collection(self, collection: Collection) -> None:
        """ Sets the collection the repository will connect to.

        Args:
            collection(Collection): Mongo collection
        """
        self.__collection = collection

    def insert_one(self, element: MongoModel) -> Union[ObjectId, str]:
        """ Method to insert one element to mongo.
        If the extended repository implements the `create_record` method,
        it can register the operation in the activity log.

        Args:
            element(MongoModel): Element to be inserted
        """
        try:
            response = self.__collection.insert_one(element.to_mongo()).inserted_id
        except DuplicateKeyError as e:
            logger.error(str(e))
            
        return response

    def insert_many(self, elements: List[MongoModel]) -> list:
        """ Method to insert multiple elements to database.

        Args:
            elements(list): List of MongoModel objects to be inserted to
                            mongo

        Returns:
            inserted_ids(int): List of ObjectIds of the inserted documents
        """
        elements = [element.to_mongo() for element in elements]
        try:
            response = self.__collection.insert_many(elements)
        except WriteError as e:
            logger.error(str(e))
            return None
        return response.inserted_ids

    def find_one(self, _filter: dict = {},
                 projection: dict = None) -> MongoModel:
        """ Method to get one element from database.

        Args:
            _filter(dict): Criteria to filter and find one element
            projection(dict): Fields to be returned or not from the found
                              element

        Returns:
            found(MongoModel): Object of the document found
        """
        found = self.__collection.find_one(
            filter=_filter,
            projection=projection
        )
        return self.model.from_mongo(found)

    def find_many(self, _filter: dict = {}, projection: dict = None,
                  sort: list = None, currentPage: int = 0,
                  pageSize: int = 0) -> List[MongoModel]:
        """ Method to get multiple elements from database.

        Args:
            _filter(dict): Criteria to filter and find multiple elements
            projection(dict): Fields to be returned or not from the found
                              elements
            sort(list): List of tuples that determines the sort field and
                        direction of the results
            currentPage(int): Field used for pagination. Specifies a specific
                              set of results to be returned.
            pageSize(int): Field used for pagination. Determines the number of
                           elements that will be returned.

        Returns:
            found(list): List of MongoModel objects of the documents found
        """
        found = self.__collection.find(
            filter=_filter,
            projection=projection,
            skip=currentPage*pageSize,
            limit=pageSize,
            sort=sort
        )
        return self.model.from_mongo(found)

    def find_all(self, _filter: dict = {}, projection: dict = None,
                  sort: list = None) -> List[MongoModel]:
        """ Method to get multiple elements from database.

        Args:
            _filter(dict): Criteria to filter and find multiple elements
            projection(dict): Fields to be returned or not from the found
                              elements
            sort(list): List of tuples that determines the sort field and
                        direction of the results

        Returns:
            found(list): List of MongoModel objects of the documents found
        """
        found = self.__collection.find(
            filter=_filter,
            projection=projection,
            sort=sort
        )
        return self.model.from_mongo(found)


    def delete_one(self, _filter: dict) -> int:
        """ Method to delete an element based on a _filter.

        Args:
            _filter(dict): Fields to filter the element to delete

        Returns:
            response(int): Number of documents deleted. Should be one for a
                           succesfull deletion.
        """
        try:
            response = self.__collection.delete_one(_filter).deleted_count
        except WriteError as e:
            logger.error(str(e))
            return None
        return response

    def logical_delete_one(self, _filter: dict) -> int:
        """ Method to make a logical delete of an element based on a _filter.

        Args:
            _filter(dict): Fields to filter the element to delete

        Returns:
            response(int): Number of documents deleted. Should be one for a
                           succesfull deletion.
        """
        try:
            response = self.__collection.update_one(
                _filter,
                {'$set': {'disabled': True}}
            ).modified_count
        except WriteError as e:
            logger.error(str(e))
            return None
        return response

    def update_one(self, _filter: dict, update: dict) -> int:
        """ Method that updates an existing element in mongo.

        Args:
            _filter(dict): Criteria to filter the document that will be
                           updated
            update(dict): Fields and values that will be updated
        """
        try:
            response = self.__collection.update_one(
                _filter,
                update
            ).modified_count
        except WriteError as e:
            logger.error(str(e))
            return None
        return response
    
    def update_many(self, _filter: dict, update: dict) -> int:
        """ Method that updates an existing element in mongo.

        Args:
            _filter(dict): Criteria to filter the document that will be
                           updated
            update(dict): Fields and values that will be updated
        """
        try:
            response = self.__collection.update(
                _filter,
                update,
                upsert=True,
                multi=True
            )
        except WriteError as e:
            logger.error(str(e))
            return None
        return response

    def aggregate(self, pipeline: list, model: MongoModel = None) -> list:
        """ Method that performs an aggregation pipeline.

        Args:
            pipeline(list): Aggregation pipeline
            model(MongoModel): If this param is provided, the retrieved
                               documents will be validated againts this model.
                               If not, will be validated againts self.model

        Returns:
            elements(list): List of aggregation results
        """
        elements = self.__collection.aggregate(pipeline)
        if model:
            return model.from_mongo(elements)
        return self.model.from_mongo(elements)
