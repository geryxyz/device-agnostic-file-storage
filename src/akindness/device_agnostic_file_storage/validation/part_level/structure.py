from networkx.classes import MultiDiGraph


def has_parts(graph: MultiDiGraph, node: str) -> bool:
    name: str = graph.nodes[node]["visibleName"]
    if name == "root":
        return True
    return name.count(".") > 0

def no_empty_parts(graph: MultiDiGraph, node: str) -> bool:
    name: str = graph.nodes[node]["visibleName"]
    return all(part.strip() != "" for part in name.split("."))

def parts_dont_start_with_underscore(graph: MultiDiGraph, node: str) -> bool:
    name: str = graph.nodes[node]["visibleName"]
    return all(part.strip() != "" and not part.strip().startswith("_") for part in name.split("."))

def parts_dont_end_with_underscore(graph: MultiDiGraph, node: str) -> bool:
    name: str = graph.nodes[node]["visibleName"]
    return all(part.strip() != "" and not part.strip().endswith("_") for part in name.split("."))