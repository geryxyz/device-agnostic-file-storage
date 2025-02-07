from networkx.classes import MultiDiGraph


def is_leaf(graph: MultiDiGraph, node: str) -> bool:
    return not any(data["type"] == "child" for _, _, data in graph.out_edges(node, data=True))