
class DefaultQueue(object):
    def __init__(self, _map, verbose=False):
        self._list = []
        self._map = _map
        self._verbose = verbose

    def add(self, location, path, distance):
        self._list.insert(0, [location, path, distance])

    def pop(self):
        if self._verbose:
            first = self._list[0]
            print('-'+'['+first[0].get_name()+','+first[1]+','+str(first[2])+']')
        return self._list.pop(0)

    def sort(self):
        self._list.sort(key=lambda x: x[2])

    def size(self):
        if self._verbose:
            print('+',end="")
            for element in self._list:
                print('['+element[0].get_name()+','+element[1]+','+str(element[2])+']',end="")
            print("\n")
        return len(self._list)


class AStarQueue(DefaultQueue):
    def sort(self):
        self._list.sort(key=lambda x: (x[2] + self._map.get_straight_line_distance(x[0].get_name())))


class GreedyQueue(AStarQueue):
    def sort(self):
        self._list.sort(key=lambda x: self._map.get_straight_line_distance(x[0].get_name()))
