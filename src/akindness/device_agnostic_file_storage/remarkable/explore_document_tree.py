import json
import shutil
from pathlib import Path

from networkx import DiGraph
from paramiko.client import SSHClient

from akindness.device_agnostic_file_storage.remarkable.authentication import get_remarkable_password, \
    get_remarkable_ip_address


REMARKABLE_DOCUMENTS_PATH = "/home/root/.local/share/remarkable/xochitl/"


def explore(temp_dir: Path = Path.cwd() / "temp"):
    download_metadata(temp_dir)
    graph: DiGraph = assemble_file_system_graph(temp_dir)


def download_metadata(temp_dir):
    client = SSHClient()
    client.load_system_host_keys()
    client.connect(
        hostname=get_remarkable_ip_address(),
        username="root",
        password=get_remarkable_password(),

    )
    sftp = client.open_sftp()
    metadata_path_collection = _get_metadata_path_collection(sftp)
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True)
    for metadata_path in metadata_path_collection:
        temp_metadata_path = temp_dir / metadata_path.split("/")[-1]
        sftp.get(metadata_path, temp_metadata_path)


def _get_metadata_path_collection(sftp) -> tuple[str, ...]:
    raw_document_path_collection = sftp.listdir(REMARKABLE_DOCUMENTS_PATH)
    metadata_path_collection = [
        REMARKABLE_DOCUMENTS_PATH + raw_document_path
        for raw_document_path in raw_document_path_collection
        if raw_document_path.endswith(".metadata")
    ]
    return tuple(metadata_path_collection)


def assemble_file_system_graph(temp_dir: Path) -> DiGraph:
    graph = DiGraph()
    for metadata_path in temp_dir.iterdir():
        if not metadata_path.is_file() or not (metadata_path.suffix == ".metadata"):
            continue
        current_id = metadata_path.stem
        graph.add_node(current_id)
    for metadata_path in temp_dir.iterdir():
        if not metadata_path.is_file() or not (metadata_path.suffix == ".metadata"):
            continue
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)
            current_id = metadata_path.stem
            metadata["id"] = current_id
            graph.add_node(current_id, **metadata)
            parent_id: str = metadata.get("parent")
            if parent_id.strip() != "":
                graph.add_edge(parent_id, current_id)
    return graph
