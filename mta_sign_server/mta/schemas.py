from pydantic import BaseModel
from typing import List, Dict

from mta_api_client import Route


class RouteResponse(BaseModel):
    arrival_times: List[int]


class StationResponse(BaseModel):
    routes: Dict[Route, RouteResponse]


class AllStationModel(BaseModel):
    stations: Dict[str, StationResponse]
