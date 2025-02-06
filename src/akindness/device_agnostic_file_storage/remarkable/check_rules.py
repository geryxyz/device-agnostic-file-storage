import re

from networkx.classes import DiGraph


def _valid_characters(graph: DiGraph, node: str) -> bool:
    return re.match(r"^[a-zA-Z0-9_.]+$", graph.nodes[node]["visibleName"]) is not None

def check(graph: DiGraph, node: str) -> bool:
    for parent in graph.predecessors(node):
        if not check(graph, parent):
            return False
    if not _valid_characters(graph, node):
        return False
    return True

def check_all(graph: DiGraph):
    for node in graph.nodes:
        is_valid = check(graph, node)
        graph.nodes[node]["valid"] = is_valid
    return graph