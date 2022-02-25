from .stop import get_stop_from_dict


def get_train_from_dict(obj):
    if "trip_update" in obj and "stop_time_update" in obj["trip_update"]:
        # data we need is here create object
        id = obj["id"]
        route = obj["trip_update"]["trip"]["route_id"]
        all_stops = [get_stop_from_dict(x) for x in obj["trip_update"]["stop_time_update"]]
        valid_stops = [valid_stop for valid_stop in all_stops if valid_stop is not None]
        return Train(id, route, valid_stops)
    else:
        return None


class Train(object):
    def __init__(self, id, route, stops):
        self.id = id
        self.route = route
        self.stops = stops

    def get_arrival_at(self, stop_id):
        """
        returns the routes stop time at a given stop ID in minutes
        if not found, returns None
        :param stop_id: stop ID of arrival station
        :return: arrival time in minutes
        """
        for stop in self.stops:
            if stop.id == stop_id:
                return stop.arrival_minutes()
        return None

    def arriving_at_station_in_time(self, station_id, max_time):
        for stop in self.stops:
            minutes_to_arrival = stop.arrival_minutes()
            if stop.id == station_id:
                if minutes_to_arrival > 0 and minutes_to_arrival < max_time:
                    return True

    def __str__(self):
        formatted_stops  = '\n'.join([str(stop) for stop in self.stops])
        return f"train_id:{self.id} | line_name:{self.route}| stops:\n {formatted_stops}"
