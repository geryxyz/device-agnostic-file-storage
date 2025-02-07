import re

from networkx.classes import MultiDiGraph
from tqdm import tqdm

from akindness.device_agnostic_file_storage.check.all_check import get_all_checks


def check(graph: MultiDiGraph, node: str) -> set[str]:
    if node == "root" or node == "trash":
        return set()
    causes = set()
    for parent, current, data in graph.in_edges(node, data=True):
        assert current == node
        if data["type"] != "child":
            continue
        causes = causes.union(check(graph, parent))
    for check_method in get_all_checks():
        if not check_method(graph, node):
            causes.add(node)
    return causes

def check_all(graph: MultiDiGraph):
    for node in tqdm(graph.nodes, desc="Checking nodes", unit="node"):
        if node == "root" or node == "trash":
            continue
        invalidity_causes = check(graph, node)
        graph.nodes[node]["valid"] = not bool(invalidity_causes)
        for cause in invalidity_causes:
            if cause == "root" or cause == "trash":
                continue
            graph.add_edge(cause, node, type="invalid")

    for node in tqdm(graph.nodes, desc="Counting badness", unit="node"):
        out_edges = graph.out_edges(node, data=True)
        badness = sum(1 for _, _, data in out_edges if data["type"] == "invalid")
        graph.nodes[node]["badness"] = badness
    return graph