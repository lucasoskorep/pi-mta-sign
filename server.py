import logging
import os
import threading

from flask import Flask, jsonify, render_template, request, abort
from mta_manager import MTA
import pandas as pd

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "SuperSecretDontEvenTryToGuessMeGGEZNoRe"
app._static_folder = os.path.abspath("templates/static/")

stops = pd.read_csv("stops.txt")
stop_ids = ["127S", "127N", "A27N", "A27S"]


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


def link_to_station(data):
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


@app.route("/mta_data", methods=["POST"])
def get_mta_data():
    global subway_data
    station = request.json["station"]
    if station in subway_data:
        return jsonify(
            subway_data[station]
        )
    else:
        abort(404)


@app.route("/stops", methods=["GET"])
def get_routes():
    return jsonify()


@app.route("/get_stop_id", methods=["POST"])
def get_stop_id():
    stop_name = request.json["stop_name"]
    rows = stops.loc[stops["stop_name"] == stop_name]
    return jsonify({"station_changed": True})


if __name__ == "__main__":
    api_key = os.getenv('MTA_API_KEY', '')

    mtaController = MTA(
        api_key,
        ["A", "C", "E", "1", "2", "3"],
        ["127S", "127N", "A27N", "A27S"]
    )


    async def mta_callback(routes):
        global subway_data
        subway_data = link_to_station(mtaController.convert_routes_to_station_first(routes))
        app.logger.info(f"Updated Subway Data - {subway_data}")


    class threadWrapper(threading.Thread):
        def __init__(self, run):
            threading.Thread.__init__(self)
            self.run = run

        def run(self):
            self.run()


    def start_mta():
        mtaController.add_callback(mta_callback)
        while True:
            try:
                mtaController.start_updates()
            except Exception as e:
                logging.info(f"Exception found in update function - {e}")


    threadLock = threading.Lock()
    threads = [threadWrapper(start_mta)]

    for t in threads:
        t.start()

    debug = os.getenv("DEBUG", 'False').lower() in ('true', '1', 't')

    app.run(host="localhost", debug=debug, port=5000)
    # Wait for all threads to complete
    for t in threads:
        t.join()
    print("Exiting Main Thread")
