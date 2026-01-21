import csv
import logging
from pathlib import Path

from fastapi import APIRouter

from mta_api_client import Route
from mta_sign_server.config.schemas import Station, StationsResponse, LinesResponse

router = APIRouter(
    tags=["config"],
)

logger = logging.getLogger("config_router")

STOPS_FILE = Path(__file__).parent.parent.parent / "stops.txt"


@router.get("/api/config")
def get_all():
    return {"config": "goes here"}


@router.get("/api/stations", response_model=StationsResponse)
def get_stations(search: str | None = None):
    """Get list of all stations, optionally filtered by search term. Deduplicates by station name."""
    stations_dict = {}

    if STOPS_FILE.exists():
        with open(STOPS_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Only include parent stations (location_type == 1)
                if row.get("location_type") == "1":
                    station_name = row["stop_name"]
                    station_id = row["stop_id"]

                    # Only add first occurrence of each station name to deduplicate
                    if station_name not in stations_dict:
                        station = Station(id=station_id, name=station_name)

                        # Filter by search term if provided
                        if search:
                            if search.lower() in station.name.lower() or search in station.id:
                                stations_dict[station_name] = station
                        else:
                            stations_dict[station_name] = station

    return StationsResponse(stations=list(stations_dict.values()))


@router.get("/api/lines", response_model=LinesResponse)
def get_lines():
    """Get list of all available train lines."""
    lines = [route.value for route in Route]
    return LinesResponse(lines=sorted(lines))
