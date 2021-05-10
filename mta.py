import requests
from typing import List


class MTA(object):
    def __init__(self, api_key: str, train_lines=None, station_ids=None, timing_callbacks=None, alert_callbacks = None):
        self.api_key = api_key
        self.train_lines = train_lines if train_lines else []
        self.station_ids = station_ids if station_ids else []
        self.timing_callbacks = timing_callbacks if timing_callbacks else []
        self.alert_callbacks = alert_callbacks if alert_callbacks else []

    def start_updates(self):
        print("starting updates")
        raise NotImplementedError("Have not implemented start updates yet")

    async def process_callbacks(self):
        raise NotImplementedError("Have not implemented callback processing yet")


    def add_train_line(self, train_line: str):
        self.train_lines.append(train_line)

    def remove_train_line(self, train_line: str):
        self.train_lines.remove(train_line)

    def add_station_id(self, station_id: str):
        self.station_ids.append(station_id)

    def remove_station_id(self, station_id: str):
        self.station_ids.remove(station_id)

    def add_callback(self, callback_func):
        self.timing_callbacks.append(callback_func)

    def remove_callback(self, callback_func):
        self.timing_callbacks.remove(callback_func)