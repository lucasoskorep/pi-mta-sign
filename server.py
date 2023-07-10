import os
from datetime import datetime

import pandas as pd
from flask_apscheduler import APScheduler
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from mta_manager import MTA, Feed, Route

load_dotenv()

app = Flask(__name__)
app.secret_key = "SuperSecretDontEvenTryToGuessMeGGEZNoRe"
app._static_folder = os.path.abspath("templates/static/")

scheduler = APScheduler()
scheduler.init_app(app)


stops = pd.read_csv("stops.txt")
start_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

ROUTES = [Route.A, Route.C, Route.E, Route.N1, Route.N2, Route.N3]
STATION_STOP_IDs = ["127S", "127N", "A27N", "A27S"]


def link_to_station(data) -> {}:
    linked_data = {}
    for key, value in data.items():
        stop_name = stops.loc[stops["stop_id"] == key]
        stop_name = stop_name["stop_name"].values[0]
        if stop_name not in linked_data:
            linked_data[stop_name] = {}
        if "N" in key:
            linked_data[stop_name]["North"] = value
        elif "S" in key:
            linked_data[stop_name]["South"] = value
    return linked_data


@app.route("/", methods=["GET"])
def index():
    # TODO: Shove this into a sqlite database
    station_names = sorted(list(set(stops["stop_name"].to_list())))
    return render_template(
        "layouts/index.html",
        station_names=station_names,
        station_1="42 St-Port Authority Bus Terminal",
        station_2="Times Sq-42 St"
    )


@app.route("/start_time", methods=["GET"])
def get_start_time():
    return start_time


@app.route("/mta_data", methods=["POST"])
async def get_mta_data():
    # if len(mtaController.trains) == 0:
    #     _ = update_trains()
    arrival_by_station_and_route = {}
    for stop_id in STATION_STOP_IDs:
        arrival_by_station_and_route[stop_id] = {}
        for route in ROUTES:
            arrival_tiems = mtaController.get_arrival_times(route, stop_id)
            if len(arrival_tiems) > 0:
                arrival_by_station_and_route[stop_id][route.value] = arrival_tiems
    return arrival_by_station_and_route


@app.route("/get_stop_id", methods=["POST"])
def get_stop_id():
    stop_name = request.json["stop_name"]
    stops.loc[stops["stop_name"] == stop_name]
    return jsonify({"station_changed": True})



if __name__ == "__main__":
    api_key = os.getenv('MTA_API_KEY', '')

    old_data = None
    last_updated = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    mtaController = MTA(
        api_key,
        feeds=[Feed.ACE, Feed.N1234567]
    )
    def update_trains():
        app.logger.debug("UPDATING TRAINS")
        mtaController.update_trains()

    scheduler.add_job("train_updater", func=update_trains, trigger="interval", seconds=10)
    scheduler.start()

    debug = os.getenv("DEBUG", 'False').lower() in ('true', '1', 't')
    app.run(host="localhost", debug=True, port=5000, use_reloader=False)

    print("Exiting Main Thread")
