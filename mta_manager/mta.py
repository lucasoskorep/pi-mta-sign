import asyncio
import requests
import json

from google.transit import gtfs_realtime_pb2
from protobuf_to_dict import protobuf_to_dict
from time import time
from train import Train


class MTA(object):
    # Create a data filter object.
    # Then be able to update that object on the fly.
    # This filter should return all possible trains and stations by default.
    # If anyhting is added it gets filtered out.
    def __init__(self, api_key: str, routes, station_ids, timing_callbacks=None, alert_callbacks=None,
                 endpoints_file="./endpoints.json", callback_frequency=10, max_arrival_time=30):
        self.header = {
            "x-api-key": api_key
        }
        self.routes = routes
        self.station_ids = station_ids
        self.timing_callbacks = timing_callbacks if timing_callbacks else []
        self.is_running = False
        self.callback_frequency = callback_frequency
        self.max_arrival_time = max_arrival_time
        with open(endpoints_file, "r") as f:
            self.endpoints = json.load(f)
        self.set_valid_endpoints()

    def set_valid_endpoints(self):
        self.valid_endpoints = {}
        for key, value in self.endpoints.items():
            valid_routes = [x for x in self.routes if x in key]
            if valid_routes:
                self.valid_endpoints[value] = valid_routes
        print(self.valid_endpoints)

    def start_updates(self):
        print("starting updates")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._get_updates())

    def stop_updates(self):
        self.is_running = False

    async def get_data(self):
        trains = []
        for endpoint, valid_lines in self.valid_endpoints.items():
            r = requests.get(endpoint, headers=self.header)
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(r.content)
            subway_feed = protobuf_to_dict(feed)['entity']
            trains.extend([train for train in [Train.get_train_from_dict(train_dict) for train_dict in subway_feed] if train is not None])
        return trains


    @staticmethod
    def get_trains_for_routes(routes, trains):
        return [train for train in trains if train.route in routes]

    @staticmethod
    def get_trains_for_route(route, trains):
        return MTA.get_trains_for_routes([route], trains)


    async def get_train_information(self):
        # Might need to not filter these trains.
        valid_trains = [train for train in await self.get_data() if True]
                        # MTA.trains_arriving_at_stations(self.train_lines, self.station_ids, train, self.max_arrival_time)]
        return valid_trains

    async def _get_updates(self):
        self.is_running = True
        while (self.is_running):
            t = time()
            data = self.get_train_information()
            data = await data
            await self.process_callbacks(data)
            await asyncio.sleep(self.callback_frequency - (time() - t))

    async def process_callbacks(self, data):
        for callback in self.timing_callbacks:
            await callback(data)

    def add_train_line(self, train_line: str):
        self.routes.append(train_line)
        self.set_valid_endpoints()

    def remove_train_line(self, train_line: str):
        self.routes.remove(train_line)
        self.set_valid_endpoints()

    def add_station_id(self, station_id: str):
        self.station_ids.append(station_id)

    def remove_station_id(self, station_id: str):
        self.station_ids.remove(station_id)

    def add_callback(self, callback_func):
        self.timing_callbacks.append(callback_func)

    def remove_callback(self, callback_func):
        self.timing_callbacks.remove(callback_func)

    def get_time_arriving_at_stations(self, trains):
        station_first = {}
        for station_id in self.station_ids:
            line_first = {}
            for route in self.routes:
                valid_trains = [train.get_arrival_at(station_id) for train in MTA.get_trains_for_route(route, trains) if train.arriving_at_station_in_time(station_id, self.max_arrival_time)]
                if valid_trains:
                    line_first[route] = valid_trains
            if line_first:
                station_first[station_id] = line_first
        return station_first
