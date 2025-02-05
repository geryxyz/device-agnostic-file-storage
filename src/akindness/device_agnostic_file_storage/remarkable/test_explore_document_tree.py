from pathlib import Path

import networkx

from akindness.device_agnostic_file_storage.remarkable.explore_document_tree import explore, assemble_file_system_graph


def test_explore_document_tree():
    explore()


def test_assemble_file_system_graph():
    graph = assemble_file_system_graph(Path.cwd() / "temp")
    networkx.write_graphml(graph, "graph.graphml")
