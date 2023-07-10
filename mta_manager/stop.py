from datetime import datetime
from google.transit import gtfs_realtime_pb2
from math import trunc


def trip_arrival_in_minutes(stop_time_update: gtfs_realtime_pb2.TripUpdate):
    return trunc(((datetime.fromtimestamp(stop_time_update.arrival.time) - datetime.now()).total_seconds()) / 60)

# class Stop(object):
#     def __init__(self, id, arrival_time, departure_time, ):
#         self.id = id
#         self.arrival_time = arrival_time
#         self.departure_time = departure_time
#
#     def arrival_minutes(self):
#         return trunc(((datetime.fromtimestamp(self.arrival_time) - datetime.now()).total_seconds()) / 60)
#
#     def __str__(self):
#         now = datetime.now()
#         time = datetime.fromtimestamp(self.arrival_time)
#         time_minutes = trunc(((time - now).total_seconds()) / 60)
#         return f"stop_id:{self.id}| arr:{time_minutes}| dep:{self.departure_time}"
#
#     @staticmethod
#     def get_stop_from_dict(obj):
#         if "arrival" in obj and "departure" in obj and "stop_id" in obj:
#             return Stop(obj["stop_id"], obj["arrival"]["time"], obj["departure"]["time"])
#         return None
