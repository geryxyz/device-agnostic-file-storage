import re

from networkx.classes import DiGraph, MultiDiGraph
from tqdm import tqdm


def _valid_characters(graph: DiGraph, node: str) -> bool:
    return re.match(r"^[a-zA-Z0-9_.]+$", graph.nodes[node]["visibleName"]) is not None

def check(graph: MultiDiGraph, node: str) -> set[str]:
    causes = set()
    for parent, current, data in graph.in_edges(node, data=True):
        assert current == node
        if data["type"] != "child":
            continue
        causes = causes.union(check(graph, parent))
    if not _valid_characters(graph, node):
        causes.add(node)
    return causes

def check_all(graph: MultiDiGraph):
    for node in tqdm(graph.nodes, desc="Checking nodes", unit="node"):
        invalidity_causes = check(graph, node)
        for cause in invalidity_causes:
            graph.add_edge(cause, node, type="invalid")
            graph.nodes[node]["valid"] = not bool(invalidity_causes)

    for node in tqdm(graph.nodes, desc="Counting badness", unit="node"):
        out_edges = graph.out_edges(node, data=True)
        badness = sum(1 for _, _, data in out_edges if data["type"] == "invalid")
        graph.nodes[node]["badness"] = badness
    return graph