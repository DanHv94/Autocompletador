from typing import Optional, Dict, List

from pydantic import BaseModel
from .mongo import MongoModel

from Levenshtein import ratio

class CitiesModel(MongoModel):
    '''
    Class that represents the schema for a City document in database.
    This class is mainly used to validate the model againsts a query with a projection.
    '''
    name: Optional[str]
    lat: Optional[str]
    long: Optional[str]
    feat_class: Optional[str]
    feat_code: Optional[str]
    country: Optional[str]
    population: Optional[str]
    score: Optional[int]

    def get_score(self, name: str):
        '''
        It assigns the similarity score between the recommended city and the client's text. 
        Levenshtein distance is used to get this score.
        '''
        self.score = round(ratio(name, self.name),2)

    def __getitem__(self, key):
        return self.score

    def __eq__(self, other):
        return self.score == other.score
    
    def __lt__(self, other):
        return self.score >= other.score

class CitiesMongo(MongoModel):
    '''
    Class that represents the schema for a City document in database. This class is used
    to validate the object against almost all fields
    '''
    id: Optional[str]
    name: Optional[str]
    ascii: Optional[str]
    alt_name: Optional[str]
    lat: Optional[str]
    long: Optional[str]
    feat_class: Optional[str]
    feat_code: Optional[str]
    country: Optional[str]
    cc2: Optional[str]
    admin1: Optional[str]
    admin2: Optional[str]
    admin3: Optional[str]
    admin4: Optional[str]
    population: Optional[str]
    elevation: Optional[str]
    dem: Optional[str]
    tz: Optional[str]
    modified_at: Optional[str]

class BaseCities(BaseModel):
    id: Optional[str]
    name: Optional[str]
    lat: Optional[str]
    long: Optional[str]
    feat_class: Optional[str]
    feat_code: Optional[str]
    country: Optional[str]
    population: Optional[str]
    
class City(BaseCities):
    score: Optional[int]

    def set_score(self, name: str):
        X = "TODO"