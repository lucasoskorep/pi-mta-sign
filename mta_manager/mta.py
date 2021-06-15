import asyncio
import requests
import json

from google.transit import gtfs_realtime_pb2
from protobuf_to_dict import protobuf_to_dict
from .route import get_route_from_dict
from time import time


class MTA(object):
    def __init__(self, api_key: str, train_lines, station_ids, timing_callbacks=None, alert_callbacks=None,
                 endpoints_file="./endpoints.json", callback_frequency=5, max_arrival_time=30):
        self.header = {
            "x-api-key": api_key
        }
        self.train_lines = train_lines
        self.station_ids = station_ids
        self.timing_callbacks = timing_callbacks if timing_callbacks else []
        # self.alert_callbacks = alert_callbacks if alert_callbacks else []
        self.is_running = False
        self.callback_frequency = callback_frequency
        self.max_arrival_time = max_arrival_time
        with open(endpoints_file, "r") as f:
            self.endpoints = json.load(f)
        self.set_valid_endpoints()

    def set_valid_endpoints(self):
        self.valid_endpoints = {}
        for key, value in self.endpoints.items():
            valid_lines = [x for x in self.train_lines if x in key]
            if valid_lines:
                self.valid_endpoints[value] = valid_lines
        print(self.valid_endpoints)

    def start_updates(self):
        print("starting updates")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._get_updates())

    def stop_updates(self):
        self.is_running = False

    async def get_data(self):
        routes = []
        for endpoint, valid_lines in self.valid_endpoints.items():
            r = requests.get(endpoint, headers=self.header)
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(r.content)
            subway_feed = protobuf_to_dict(feed)['entity']
            routes.extend([x for x in [get_route_from_dict(x) for x in subway_feed] if x is not None])
        return routes

    @staticmethod
    def valid_route(train_lines, station_ids, route, max_time):
        if route.route_id not in train_lines:
            return False
        stops = route.stop_times
        for stop in stops:
            minutes_to_arrival = stop.arrival_minutes()
            if stop.stop_id in station_ids:
                if minutes_to_arrival > 0 and minutes_to_arrival < max_time:
                    return True
        return False

    async def get_route_information(self):
        # Filter routes
        valid_routes = [route for route in await self.get_data() if
                        MTA.valid_route(self.train_lines, self.station_ids, route, self.max_arrival_time)]
        return valid_routes

    async def _get_updates(self):
        self.is_running = True
        while (self.is_running):
            t = time()
            data = self.get_route_information()
            data = await data
            await self.process_callbacks(data)
            await asyncio.sleep(self.callback_frequency - (time() - t))
            # self.is_running = False

    async def process_callbacks(self, data):
        for callback in self.timing_callbacks:
            await callback(data)

    def add_train_line(self, train_line: str):
        self.train_lines.append(train_line)
        self.set_valid_endpoints()

    def remove_train_line(self, train_line: str):
        self.train_lines.remove(train_line)
        self.set_valid_endpoints()

    def add_station_id(self, station_id: str):
        self.station_ids.append(station_id)

    def remove_station_id(self, station_id: str):
        self.station_ids.remove(station_id)

    def add_callback(self, callback_func):
        self.timing_callbacks.append(callback_func)

    def remove_callback(self, callback_func):
        self.timing_callbacks.remove(callback_func)

    def convert_routes_to_station_first(self, routes):
        station_first = {}
        for station_id in self.station_ids:
            line_first = {}
            for train_line in self.train_lines:
                valid_routes = [route.get_arrival_at(station_id) for route in routes if
                                self.valid_route([train_line], [station_id], route, self.max_arrival_time)]
                if valid_routes:
                    line_first[train_line] = valid_routes
            if line_first:
                station_first[station_id] = line_first
        return station_first
