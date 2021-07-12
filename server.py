import os
import threading
from flask import Flask, jsonify, render_template, request
from mta_manager import MTA
from pprint import pprint

app = Flask(__name__)
app.secret_key = "SuperSecretDontEvenTryToGuessMeGGEZNoRe"
app.debug = True
app._static_folder = os.path.abspath("templates/static/")

subway_data = {}

@app.route("/", methods=["GET"])
def index():
    title = "Create the input image"
    return render_template("layouts/index.html", title=title)


@app.route("/mta_data", methods=["POST"])
def get_mta_data():
    content = request.json
    return jsonify(
        subway_data
    )

@app.route("/stops", methods=["GET"])
def get_routes():
    return jsonify()

if __name__ == "__main__":
    api_key = os.getenv('MTA_API_KEY', '')
    mtaController = MTA(
        api_key,
        ["A", "C", "E", "1", "2", "3"],
        ["127S", "127N", "A27N", "A27S"]
    )


    async def mta_callback(routes):
        global subway_data
        # TODO: Do away with this and throw it into websockets
        subway_data = mtaController.convert_routes_to_station_first(routes)


    class threadWrapper(threading.Thread):
        def __init__(self, run):
            threading.Thread.__init__(self)
            self.run = run

        def run(self):
            self.run()


    def start_mta():
        mtaController.add_callback(mta_callback)
        mtaController.start_updates()


    threadLock = threading.Lock()
    threads = [threadWrapper(start_mta)]

    for t in threads:
        t.start()

    app.run("0.0.0.0", port=5000, debug=True)
    # Wait for all threads to complete
    for t in threads:
        t.join()
    print("Exiting Main Thread")
