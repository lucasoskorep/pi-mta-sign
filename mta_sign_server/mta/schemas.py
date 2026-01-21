from pydantic import BaseModel
from typing import List

from mta_api_client import Route


class RouteResponse(BaseModel):
    routeId: Route
    arrival_times: List[int]


class StationResponse(BaseModel):
    stationId: str
    routes: List[RouteResponse]


class AllStationResponse(BaseModel):
    stations: List[StationResponse]
