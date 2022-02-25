
from datetime import datetime
from math import trunc

def get_stop_from_dict(obj):
    if "arrival" in obj and "departure" in obj and "stop_id" in obj:
        return Stop( obj["stop_id"], obj["arrival"]["time"], obj["departure"]["time"])
    return None


class Stop(object):
    def __init__(self, id, arrival_time, departure_time, ):
        self.id = id
        self.arrival_time = arrival_time
        self.departure_time = departure_time

    def arrival_minutes(self):
        return trunc(((datetime.fromtimestamp(self.arrival_time) - datetime.now()).total_seconds()) / 60)

    def __str__(self):
        now = datetime.now()
        time = datetime.fromtimestamp(self.arrival_time)
        time_minutes = trunc(((time - now).total_seconds()) / 60)
        return f"stop_id:{self.id}| arr:{time_minutes}| dep:{self.departure_time}"
