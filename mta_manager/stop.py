from datetime import datetime
from google.transit import gtfs_realtime_pb2
from math import trunc


def trip_arrival_in_minutes(stop_time_update: gtfs_realtime_pb2.TripUpdate):
    return trunc(((datetime.fromtimestamp(stop_time_update.arrival.time) - datetime.now()).total_seconds()) / 60)
