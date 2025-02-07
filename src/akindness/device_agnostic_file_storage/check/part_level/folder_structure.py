from networkx.classes import MultiDiGraph

from akindness.device_agnostic_file_storage.util.graph.structure import is_leaf


def first_part_is_index(graph: MultiDiGraph, node: str) -> bool:
    if is_leaf(graph, node):
        return True
    name: str = graph.nodes[node]["visibleName"]
    return name.split(".")[0].isnumeric()