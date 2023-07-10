from google.transit import gtfs_realtime_pb2
from .stop import trip_arrival_in_minutes
from .route import Route, is_valid_route


class Train(object):
    def __init__(self, train_proto: gtfs_realtime_pb2.FeedEntity):
        self.train_proto: gtfs_realtime_pb2.FeedEntity = train_proto

    def get_arrival_at(self, stop_id) -> int | None:
        """
        returns the routes stop time at a given stop ID in minutes
        if not found, returns None
        :param stop_id: stop ID of arrival station
        :return: arrival time in minutes
        """
        for stop_time_update in self.train_proto.trip_update.stop_time_update:
            if stop_time_update.stop_id == stop_id:
                return trip_arrival_in_minutes(stop_time_update)
        return None


    def _get_route(self) -> str:
        return self.train_proto.trip_update.trip.route_id
    def get_route(self) -> Route:
       return Route(self.train_proto.trip_update.trip.route_id)

    def has_trips(self) -> bool:
        return self.train_proto.trip_update is not None \
            and len(self.train_proto.trip_update.stop_time_update) > 0 and is_valid_route(self._get_route())

    def __str__(self):
        return f"{self.train_proto}"

