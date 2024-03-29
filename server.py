import os
import threading
import pandas as pd

from deepdiff import DeepDiff
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, abort
from mta_manager import MTA

load_dotenv()

app = Flask(__name__)
app.secret_key = "SuperSecretDontEvenTryToGuessMeGGEZNoRe"
app._static_folder = os.path.abspath("templates/static/")

stops = pd.read_csv("stops.txt")
stop_ids = ["127S", "127N", "A27N", "A27S"]

start_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")


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
def get_mta_data():
    global subway_data
    station = request.json["station"]
    if station in subway_data:
        mta_data = subway_data[station]
        mta_data["LastUpdated"] = subway_data["LastUpdated"]
        return jsonify(
            mta_data
        )
    else:
        abort(404)


@app.route("/stops", methods=["GET"])
def get_routes():
    return jsonify()


@app.route("/get_stop_id", methods=["POST"])
def get_stop_id():
    stop_name = request.json["stop_name"]
    stops.loc[stops["stop_name"] == stop_name]
    return jsonify({"station_changed": True})


if __name__ == "__main__":
    api_key = os.getenv('MTA_API_KEY', '')

    old_data = None
    last_updated = datetime.now().strftime("%d/%m/%Y %H:%M:%S")


    async def mta_callback(trains):
        global subway_data, old_data, last_updated
        subway_data = link_to_station(mtaController.get_time_arriving_at_stations(trains))
        subway_data["LastUpdated"] = last_updated
        if old_data is None:
            old_data = subway_data
        data_diff = DeepDiff(old_data, subway_data, ignore_order=True)
        if data_diff != {}:
            old_data = subway_data
            last_updated = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        app.logger.info(f"Updated Subway Data - {subway_data}")


    class threadWrapper(threading.Thread):
        def __init__(self, run):
            threading.Thread.__init__(self)
            self.run = run

        def run(self):
            self.run()


    mtaController = MTA(
        api_key,
        ["A", "C", "E", "1", "2", "3"],
        ["127S", "127N", "A27N", "A27S"]
    )
    mtaController.add_callback(mta_callback)


    def start_mta():
        while True:
            try:
                mtaController.start_updates()
            except Exception as e:
                app.logger.info(f"Exception found in update function - {e}")


    threadLock = threading.Lock()
    threads = [threadWrapper(start_mta)]

    for t in threads:
        t.start()

    debug = os.getenv("DEBUG", 'False').lower() in ('true', '1', 't')
    app.run(host="localhost", debug=True, port=5000)

    for t in threads:
        t.join()
    print("Exiting Main Thread")
