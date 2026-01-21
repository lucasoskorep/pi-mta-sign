import csv
import logging
import os
from pathlib import Path
from collections import defaultdict

from fastapi import APIRouter, HTTPException
from fastapi_utils.tasks import repeat_every
from starlette import status

from mta_api_client import Route, MTA
from mta_api_client.feed import ALL_FEEDS
from mta_sign_server.mta.schemas import StationResponse, RouteResponse, AllStationResponse

router = APIRouter(
    tags=["mta-data"],
)

logger = logging.getLogger("mta")

api_key = os.getenv('MTA_API_KEY', '')

mtaController = MTA(
    api_key,
    feeds=ALL_FEEDS
)

ROUTES = [member for member in Route]
STATION_STOP_IDs = ["127S", "127N", "A27N", "A27S"]
STOPS_FILE = Path(__file__).parent.parent.parent / "stops.txt"

# Build mappings for station resolution
_station_name_to_ids = None
_station_id_to_name = None


def _load_station_mapping():
    global _station_name_to_ids, _station_id_to_name
    if _station_name_to_ids is not None:
        return

    _station_name_to_ids = defaultdict(set)
    _station_id_to_name = {}

    if STOPS_FILE.exists():
        with open(STOPS_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("location_type") == "1":  # Parent stations only
                    station_name = row["stop_name"]
                    station_id = row["stop_id"]
                    _station_name_to_ids[station_name].add(station_id)
                    _station_id_to_name[station_id] = station_name


def _resolve_base_station_ids(stop_id: str) -> list[str]:
    """Resolve a stop_id to a list of all base parent station IDs (without direction) that share the same station name."""
    _load_station_mapping()

    # Remove direction suffix to get base ID
    base_id = stop_id.rstrip("NS")

    # Look up the station name for this ID
    if base_id in _station_id_to_name:
        station_name = _station_id_to_name[base_id]
        # Return all base station IDs with this name
        return sorted(list(_station_name_to_ids[station_name]))

    # If not found, just return the base ID
    return [base_id]


@router.post("/api/mta/{stop_id}/{route}", response_model=RouteResponse, status_code=status.HTTP_200_OK)
def get_route(stop_id: str, route: Route):
    arrival_times = mtaController.get_arrival_times(route, stop_id)
    if len(arrival_times) > 0:
        return RouteResponse(routeId=route, arrival_times=arrival_times)
    raise HTTPException(status_code=404, detail="no stops found for route and stop id")


@router.post("/api/mta/{stop_id}", response_model=StationResponse, status_code=status.HTTP_200_OK)
def get_station(stop_id: str):
    routes_dict = {}  # Use dict to avoid duplicates
    base_station_ids = _resolve_base_station_ids(stop_id)

    # Extract the requested direction
    requested_direction = ""
    if stop_id.endswith("N"):
        requested_direction = "N"
    elif stop_id.endswith("S"):
        requested_direction = "S"

    # Only query the requested direction for each base station ID
    for base_id in base_station_ids:
        station_id_with_direction = f"{base_id}{requested_direction}"
        for route in ROUTES:
            arrival_times = mtaController.get_arrival_times(route, station_id_with_direction)
            if len(arrival_times) > 0:
                route_key = route.value
                if route_key not in routes_dict:
                    routes_dict[route_key] = (route, arrival_times)
                else:
                    # Combine arrival times from different station IDs
                    routes_dict[route_key] = (route, sorted(list(set(routes_dict[route_key][1] + arrival_times))))

    routes = [RouteResponse(routeId=route, arrival_times=times) for route, times in routes_dict.values()]

    if routes:
        return StationResponse(stationId=stop_id, routes=routes)
    raise HTTPException(status_code=404, detail="no trains or routes found for stop id")


@router.post("/api/mta", response_model=AllStationResponse, status_code=status.HTTP_200_OK)
def get_all():
    print("HELLO WORLD")
    all_stations = []
    for stop_id in STATION_STOP_IDs:
        routes = []
        for route in ROUTES:
            arrival_times = mtaController.get_arrival_times(route, stop_id)
            if len(arrival_times) > 0:
                routes.append(RouteResponse(routeId=route, arrival_times=arrival_times))
        all_stations.append(StationResponse(stationId=stop_id, routes=routes))
    print(all_stations)
    if all_stations:
        return AllStationResponse(stations=all_stations)
    raise HTTPException(status_code=404, detail="no arriving trains found for all configured routes")


@router.on_event("startup")
@repeat_every(seconds=10)
def update_trains():
    logger.info("UPDATING TRAINS")
    mtaController.update_trains()
