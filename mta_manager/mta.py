import requests

from google.transit import gtfs_realtime_pb2
from .train import Train
from .feed import Feed, ALL_FEEDS
from .route import Route


class MTA(object):
    def __init__(self, api_key: str, feeds: [Feed] = ALL_FEEDS, stations: [str] = [],
                 max_arrival_time: int = 30):
        self.header = {
            "x-api-key": api_key
        }
        self.feeds = feeds
        self.stations = stations
        self.max_arrival_time = max_arrival_time
        self.trains: [Train] = []

    def stop_updates(self):
        self.is_running = False

    def update_trains(self) -> [Train]:
        trains = []
        for feed in self.feeds:
            r = requests.get(feed.value, headers=self.header)
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(r.content)
            trains.extend([train for train in [Train(train) for train in feed.entity] if
                           train.has_trips()])
        self.trains = trains
        return trains

    def get_trains(self) -> [Train]:
        return self.trains

    def get_arrival_times(self, route: Route, station: str) -> [int]:
        arrival_times = []
        for train in self.trains:
            if train.get_route() is route:
                arrival = train.get_arrival_at(station)
                if arrival is not None and arrival < self.max_arrival_time and arrival > 0:
                    arrival_times.append(arrival)
        return sorted(arrival_times)

    def add_station_id(self, station_id: str):
        self.stations.append(station_id)

    def remove_station_id(self, station_id: str):
        self.stations.remove(station_id)
