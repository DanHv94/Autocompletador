from logging import getLogger
from logging import getLogger

from typing import List
from fastapi import Depends
from pymongo.database import Database
from repositories.generic import MongoRepository

from contexts import get_mongo
from models.pydantic.cities import CitiesModel, CitiesMongo, BaseCities, City

logger = getLogger()

class CitiesRepository(MongoRepository):

    def __init__(self, db: Database = Depends(get_mongo)):
        super().__init__()
        self.set_collection(db.get_collection("cities"))
        self.model = CitiesModel

    def get_cities(self, filter: str, projection: dict = None) -> List[CitiesModel]:
        '''
        Gets cities coincidences
        '''
        query = {
            "name": {
                "$regex": filter,
                "$options": "i"
            }
        }
        cities = self.find_many(query, projection)
        cities = self.get_cities_score(cities, filter)
        return cities

    def get_cities_score(self, cities: List[CitiesModel], name: str):
        '''
        Get each suggested city a score [0,1] according to its similarity to the client's text
        '''
        for city in cities:
            city.get_score(name)
        sorted_cities = sorted(cities)
        return sorted_cities

