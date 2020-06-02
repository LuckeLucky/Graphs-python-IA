import exceptions


class Location(object):

    def __init__(self, name):
        self._name = name
        self._paths = {}

    def get_name(self):
        return self._name

    def add_adjacent_path(self, destination, distance):
        self._paths[destination] = distance

    def get_adjacent_distance(self, destination):
        if destination not in self._paths:
            raise exceptions.InexistentLocationError
        return self._paths[destination]

    def get_paths(self):
        return self._paths.keys()
