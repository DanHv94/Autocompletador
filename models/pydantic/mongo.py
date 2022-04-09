""" File that contains classes to extend pydantic capabilities with MongoDB.

For more info visit https://github.com/tiangolo/fastapi/issues/1515
"""
from datetime import datetime

from bson.objectid import ObjectId
from bson.errors import InvalidId
from pydantic import BaseModel, BaseConfig

from pymongo.cursor import Cursor
from pymongo.command_cursor import CommandCursor


class OID(str):
    """ Class to define a pydantic type to validate Mongo ObjectIDs
    """
    @classmethod
    def __get_validators__(cls):
        """ Class method that returns the desired validation functio when
        validation is needed.

        Returns:
            cls.validate(function): OID.validate function
        """
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """ Class method that validates if the input is a valid Mongo ObjectId

        Args:
            v: Input value

        Returns:
            (ObjectId): Mongo ObjectId object

        Raises:
            ValueError: When the input is not a valid mongo ObjectId
        """
        try:
            return ObjectId(str(v))
        except InvalidId:
            raise ValueError("Not a valid ObjectId")


class MongoModel(BaseModel):
    """ Class that extends pydantic BaseModel class to make it Mongo friendly.
    """
    class Config(BaseConfig):
        """ Class to define custom configuration for fields validation.
        """
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(), # pylint: disable=W0108
            ObjectId: lambda oid: str(oid) # pylint: disable=W0108
        }

    @classmethod
    def from_mongo(cls, data):
        """ Class method to transform mongo data into pydantic friendly format.

        Args:
            data: Data from mongo

        Returns:
            pydantic object or list of pydantic objects
        """
        if not data:
            return data
        if isinstance(data, (Cursor, CommandCursor)):
            list_data = []
            for d in data:
                id = d.pop('_id', None) # pylint: disable=W0622
                res = cls(**dict(d, id=id))
                list_data.append(res)
            return list_data
        id = data.pop('_id', None)
        return cls(**dict(data, id=id))

    def to_mongo(self, **kwargs) -> dict:
        """ Object method that transforms pydantic data into mongo friendly
        format.

        Returns:
            parsed(dict): kwargs info in mongo friendly format
        """
        exclude_unset = kwargs.pop('exclude_unset', True)
        by_alias = kwargs.pop('by_alias', True)

        parsed = self.dict(
            exclude_unset=exclude_unset,
            by_alias=by_alias,
            **kwargs
        )

        if '_id' not in parsed and 'id' in parsed:
            parsed['_id'] = parsed.pop('id')

        return parsed
