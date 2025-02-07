from networkx.classes import MultiDiGraph


class UniqueMultiDiGraph(MultiDiGraph):
    def __init__(self):
        super().__init__()
        self._last_edge_key = 0

    def new_edge_key(self, u, v):
        self._last_edge_key += 1
        return self._last_edge_key