import re

import argparse
from pathlib import Path
from typing import cast

import networkx
from networkx.classes import MultiDiGraph
from tqdm import tqdm
import structlog

from akindness.device_agnostic_file_storage.validation.all_validators import get_all_validators

logger = structlog.stdlib.get_logger()


def validate(graph: MultiDiGraph, node: str) -> set[str]:
    if node == "root" or node == "trash":
        return set()
    causes = set()
    for parent, current, data in graph.in_edges(node, data=True):
        assert current == node
        if data["type"] != "child":
            continue
        causes = causes.union(validate(graph, parent))
    for validator in get_all_validators():
        if not validator(graph, node):
            causes.add(node)
    return causes

def validate_all(graph: MultiDiGraph):
    for node in tqdm(graph.nodes, desc="validating nodes", unit="node"):
        if node == "root" or node == "trash":
            continue
        invalidity_causes = validate(graph, node)
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("graphml", type=Path)
    parser.add_argument("--output", type=Path, required=False, default=None)
    args = parser.parse_args()

    if not cast(Path, args.graphml).is_file():
        logger.error(f"File {args.graphml} does not exist")
        exit(1)

    if args.output is None:
        args.output = Path(re.sub(r"\.graphml$", "_validated.graphml", str(args.graphml)))

    graph = networkx.read_graphml(args.graphml)
    graph = validate_all(graph)
    networkx.write_graphml(graph, args.output)
