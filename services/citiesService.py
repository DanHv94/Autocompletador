import logging
from typing import List

from fastapi import Depends

from models.pydantic.cities import BaseCities, City
from repositories.citiesRepository import CitiesRepository

logger = logging.getLogger(__name__)

class CitiesService():
    def __init__(self, repository: CitiesRepository = Depends()):
        self.__repository = repository
    
    def get_cities(self, name: str = "") -> List[City]:
        projection = {"_id": 0, "name": 1, "lat": 1, "long": 1, 
        "feat_class": 1, "feat_code": 1, "country": 1, "population": 1}
        cities = self.__repository.get_cities(name, projection)
        return cities