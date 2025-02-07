import re

from networkx.classes import MultiDiGraph


def valid_characters(graph: MultiDiGraph, node: str) -> bool:
    return re.match(r"^[a-zA-Z0-9_.]+$", graph.nodes[node]["visibleName"]) is not None
