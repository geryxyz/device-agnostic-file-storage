from pathlib import Path

import networkx

from akindness.device_agnostic_file_storage.remarkable.check_rules import check_all
from akindness.device_agnostic_file_storage.remarkable.explore_document_tree import assemble_file_system_graph


def test_check_all():
    graph = assemble_file_system_graph(Path.cwd() / "temp")
    graph = check_all(graph)
    networkx.write_graphml(graph, "graph.graphml")