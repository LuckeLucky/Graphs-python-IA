import json

import exceptions
from location import Location
from queues import *


class Map(object):
    def __init__(self, file):
        self._locations = {}
        self._distance_straight_faro = {}
        with open(file, encoding='utf-8') as json_file:
            data = json.load(json_file)

            self._name = data['name']

            # First add all cities
            for location in data['locations']:
                self.add_location(location['name'])

            # Add all paths between location
            for location in data['locations']:
                self.add_straigh_line(location['name'], location['straight'])
                for path in location['paths']:
                    self.add_path(location['name'], path['name'], path['distance'])

    def add_location(self, location_name):
        location = Location(location_name)
        self._locations[location_name] = location

    def add_path(self, source_name, destination_name, distance):
        if source_name not in self._locations:
            raise exceptions.InexistentLocationError
        if destination_name not in self._locations:
            raise exceptions.InexistentLocationError
        self._locations[source_name].add_adjacent_path(self._locations[destination_name], distance)
        self._locations[destination_name].add_adjacent_path(self._locations[source_name], distance)

    def add_straigh_line(self, source_name, distance):
        self._distance_straight_faro[source_name] = distance

    def get_location(self, location_name):
        if location_name not in self._locations:
            raise exceptions.InexistentLocationError
        return self._locations[location_name]

    def get_straight_line_distance(self, location_name):
        if location_name not in self._locations:
            raise exceptions.InexistentLocationError
        return self._distance_straight_faro[location_name]

    def uniform_cost_search(self, source_name, destination_name, verbose):
        source = self.get_location(source_name)
        destination = self.get_location(destination_name)

        queue = DefaultQueue(self,verbose)
        queue.add(source, source.get_name(), 0)

        while queue.size() != 0:

            current, current_path, distance = queue.pop()

            if current.get_name() == destination_name:
                return [current_path,str(distance)]
            else:
                for next_location in current.get_paths():
                    if next_location.get_name() in current_path:
                        continue
                    next_path = current_path + '->' + next_location.get_name()
                    distance_to_destination = distance + current.get_adjacent_distance(next_location)
                    queue.add(next_location, next_path, distance_to_destination)

                queue.sort()
        raise exceptions.PathNotFoundError

    def limited_depth(self, source_name, destination_name, limit, verbose):
        source = self.get_location(source_name)
        destination = self.get_location(destination_name)

        queue = DefaultQueue(self,verbose)

        queue.add(source, source.get_name(), 0)

        current_depth = 0

        while queue.size() != 0:
            if current_depth <= limit:
                current, current_path, distance = queue.pop()
                if current.get_name() == destination_name:
                    return [current_path,str(distance)]
                else:
                    for next_location in current.get_paths():
                        if next_location.get_name() in current_path:
                            continue
                        next_path = current_path + '->' + next_location.get_name()
                        distance_to_destination = distance + current.get_adjacent_distance(next_location)
                        queue.add(next_location, next_path, distance_to_destination)
                    current_depth += 1
            else:
                raise exceptions.PathNotFoundError

    def a_star(self, source_name, verbose):
        source = self.get_location(source_name)

        queue = AStarQueue(self,verbose)

        queue.add(source, source.get_name(), 0)

        while queue.size() != 0:
            current, current_path, distance = queue.pop()

            if current.get_name() == 'Faro':
                return [current_path,str(distance)]

            else:
                for next_location in current.get_paths():
                    if next_location.get_name() in current_path:
                        continue
                    next_path = current_path + '->' + next_location.get_name()
                    distance_to_destination = distance + current.get_adjacent_distance(next_location)
                    queue.add(next_location, next_path, distance_to_destination)

            queue.sort()

    def greedy_search(self,source_name, verbose):
        source = self.get_location(source_name)

        queue = GreedyQueue(self,verbose)

        queue.add(source, source.get_name(), 0)

        while queue.size() != 0:
            current, current_path, distance = queue.pop()

            if current.get_name() == 'Faro':
                return [current_path,str(distance)]

            else:
                for next_location in current.get_paths():
                    if next_location.get_name() in current_path:
                        continue
                    next_path = current_path + '->' + next_location.get_name()
                    distance_to_destination = distance + current.get_adjacent_distance(next_location)
                    queue.add(next_location, next_path, distance_to_destination)

            queue.sort()

