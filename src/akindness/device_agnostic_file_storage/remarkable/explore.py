import argparse
from pathlib import Path
from typing import cast

import networkx

from akindness.device_agnostic_file_storage.remarkable.explore_document_tree import explore

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--overwrite", action="store_true", required=False, default=False)
    args = parser.parse_args()

    if cast(Path, args.output).exists():
        print("Output file already exists")
        if not args.overwrite:
            exit(1)

    graph = explore()
    networkx.write_graphml(graph, args.output)
