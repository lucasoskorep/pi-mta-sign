import logging
import os

from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every


# import pandas as pd
from dotenv import load_dotenv

from mta_manager import MTA, Feed, Route

load_dotenv()


api_key = os.getenv('MTA_API_KEY', '')

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

logger = logging.getLogger(__name__)  # the __name__ resolve to "main" since we are at the root of the project.


start_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
last_updated = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

mtaController = MTA(
    api_key,
    feeds=[Feed.ACE, Feed.N1234567]
)

ROUTES = [Route.A, Route.C, Route.E, Route.N1, Route.N2, Route.N3]
STATION_STOP_IDs = ["127S", "127N", "A27N", "A27S"]


@app.post("/api/start_time")
def get_start_time():
    return start_time

@app.post("/api/mta_data")
async def get_mta_data():
    # if len(mtaController.trains) == 0:
    #     _ = update_trains()
    arrival_by_station_and_route = {}
    for stop_id in STATION_STOP_IDs:
        arrival_by_station_and_route[stop_id] = {}
        for route in ROUTES:
            arrival_times = mtaController.get_arrival_times(route, stop_id)
            if len(arrival_times) > 0:
                arrival_by_station_and_route[stop_id][route.value] = arrival_times
    return arrival_by_station_and_route

@app.on_event("startup")
@repeat_every(seconds=5)
async def update_trains():
    logger.info("UPDATING TRAINS")
    mtaController.update_trains()
