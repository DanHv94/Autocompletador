from logging import getLogger

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from starlette.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR)

from models.pydantic.cities import BaseCities, City
from services import CitiesService

router = APIRouter()
logger = getLogger(__name__)

@router.get("/search")
async def get_cities(q: str, service: CitiesService = Depends()):
    """
    Endpoint that gets all the cities that can autocomplete the search
    
    Query parameters:
    ---
    q(string): Part of the city's name
    """
    cities = service.get_cities(q)
    return cities
