import logging
import os

from fastapi import APIRouter, HTTPException
from fastapi_utils.tasks import repeat_every
from starlette import status

from mta_api_client import Route, MTA, Feed
from mta_sign_server.mta.schemas import StationResponse, RouteResponse, AllStationModel

router = APIRouter(
    tags=["mta-data"],
)

logger = logging.getLogger("mta")

api_key = os.getenv('MTA_API_KEY', '')

mtaController = MTA(
    api_key,
    feeds=[Feed.ACE, Feed.N1234567]
)

ROUTES = [Route.A, Route.C, Route.E, Route.N1, Route.N2, Route.N3]
STATION_STOP_IDs = ["127S", "127N", "A27N", "A27S"]


@router.post("/api/mta/{stop_id}/{route}", response_model=RouteResponse, status_code=status.HTTP_200_OK)
def get_route(stop_id: str, route: Route):
    arrival_times = mtaController.get_arrival_times(route, stop_id)
    if len(arrival_times) > 0:
        return RouteResponse(arrival_times=arrival_times)
    raise HTTPException(status_code=404, detail="no stops found for route and stop id")


@router.post("/api/mta/{stop_id}", response_model=StationResponse, status_code=status.HTTP_200_OK)
def get_station(stop_id: str):
    routes = {}
    for route in ROUTES:
        arrival_times = mtaController.get_arrival_times(route, stop_id)
        if len(arrival_times) > 0:
            routes[route] = RouteResponse(arrival_times=arrival_times)
    if routes:
        return StationResponse(routes=routes)
    raise HTTPException(status_code=404, detail="no trains or routes found for stop id")


@router.post("/api/mta", response_model=AllStationModel, status_code=status.HTTP_200_OK)
def get_all():
    print("HELLO WORLD")
    all_stations = {}
    for stop_id in STATION_STOP_IDs:
        routes = {}
        for route in ROUTES:
            arrival_times = mtaController.get_arrival_times(route, stop_id)
            if len(arrival_times) > 0:
                routes[route] = RouteResponse(arrival_times=arrival_times)
        all_stations[stop_id] = StationResponse(routes=routes)
    if all_stations:
        return AllStationModel(stations=all_stations)
    raise HTTPException(status_code=404, detail="no arriving trains found for all configured routes")


@router.on_event("startup")
@repeat_every(seconds=10)
def update_trains():
    logger.info("UPDATING TRAINS")
    mtaController.update_trains()
