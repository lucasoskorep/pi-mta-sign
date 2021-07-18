import os
import threading
from flask import Flask, jsonify, render_template, request
from mta_manager import MTA
from pprint import pprint
import pandas as pd

app = Flask(__name__)
app.secret_key = "SuperSecretDontEvenTryToGuessMeGGEZNoRe"
app.debug = True
app._static_folder = os.path.abspath("templates/static/")

subway_data = {}

stops = pd.read_csv("stops.txt")


@app.route("/", methods=["GET"])
def index():
    # TODO: Shove this into a sqlite database
    station_names = sorted(list(set(stops["stop_name"].to_list())))
    print(station_names)
    return render_template("layouts/index.html", station_names=station_names)


@app.route("/mta_data", methods=["POST"])
def get_mta_data():
    content = request.json
    return jsonify(
        subway_data
    )


@app.route("/stops", methods=["GET"])
def get_routes():
    return jsonify()

@app.route("/get_stop_id/<stop_name>", methods=["GET"])
def get_stop_id(stop_name):
    print(stop_name)
    rows = stops.loc[stops["stop_name"] == stop_name]
    print(rows)
    return str(rows)



def ack():
    print('message was received!')


class threadWrapper(threading.Thread):
    def __init__(self, run, controller):
        threading.Thread.__init__(self)
        self.run = run
        self.controller = controller

    def run(self):
        self.run()


async def mta_callback(routes):
    global subway_data
    # TODO: Do away with this and throw it into websockets
    subway_data = mtaController.convert_routes_to_station_first(routes)


def start_mta():
    mtaController.add_callback(mta_callback)
    mtaController.start_updates()


if __name__ == "__main__":
    api_key = os.getenv('MTA_API_KEY', '')
    mtaController = MTA(
        # TODO: Update to only work with station names - need to be able to transfer the station names to train lines -
        #  maybe with polling the station ids to see what train lines come up?
        api_key,
        ["A", "C", "E", "1", "2", "3"],
        ["127S", "127N", "A27N", "A27S"]
    )
    threadLock = threading.Lock()
    threads = [threadWrapper(start_mta, mtaController)]

    for t in threads:
        t.start()

    app.run("0.0.0.0", port=5000, debug=True)
    # Wait for all threads to complete
    for t in threads:
        t.join()
    print("Exiting Main Thread")
