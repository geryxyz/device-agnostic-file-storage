from pathlib import Path

import networkx

from akindness.device_agnostic_file_storage.remarkable.explore_document_tree import assemble_file_system_graph
from akindness.device_agnostic_file_storage.validation.validate import validate_all


def test_validate_all():
    graph = assemble_file_system_graph(Path.cwd() / "temp")
    graph = validate_all(graph)
    networkx.write_graphml(graph, "graph.graphml")