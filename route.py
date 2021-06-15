from stop import get_stop_from_dict


def get_route_from_dict(obj):
    if "trip_update" in obj and "stop_time_update" in obj["trip_update"]:
        # data we need is here create object
        id = obj["id"]
        route_id = obj["trip_update"]["trip"]["route_id"]
        stop_times = [valid_stop for valid_stop in
                      [get_stop_from_dict(x) for x in obj["trip_update"]["stop_time_update"]]
                      if valid_stop is not None]
        return Route(id, route_id, stop_times)
    else:
        return None


class Route(object):
    def __init__(self, id, route_id, stop_times):
        self.id = id
        self.route_id = route_id
        self.stop_times = stop_times

    def get_arrival_at(self, stop_id):
        """
        returns the routes stop time at a given stop ID in minutes
        if not found, returns None
        :param stop_id: stop ID of arrival station
        :return: arrival time in minutes
        """
        for stop in self.stop_times:
            if stop.stop_id == stop_id:
                return stop.arrival_minutes()
        return None

    def __str__(self):
        return f"id:{self.id} | route_id:{self.route_id}| stop_times:{self.stop_times}"
