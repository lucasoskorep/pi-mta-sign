from time import time
from datetime import datetime
from math import trunc

def get_stop_from_dict(obj):
    if "arrival" in obj and "departure" in obj and "stop_id" in obj:
        return Stop(obj["arrival"]["time"], obj["departure"]["time"], obj["stop_id"])
    return None


class Stop(object):
    def __init__(self, arrival_time, departure_time, stop_id):
        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.stop_id = stop_id

    def arrival_minutes(self):
        return trunc(((datetime.fromtimestamp(self.arrival_time) - datetime.now()).total_seconds()) / 60)

    def __str__(self):
        now = datetime.now()
        time = datetime.fromtimestamp(self.arrival_time)
        time_minutes = trunc(((time - now).total_seconds()) / 60)
        return f"arr:{time_minutes}|dep:{self.departure_time}|stop_id:{self.stop_id}"
