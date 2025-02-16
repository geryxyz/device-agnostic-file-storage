import json
import shutil
from pathlib import Path

from networkx import DiGraph
from networkx.classes import MultiDiGraph
from paramiko.client import SSHClient
from paramiko.sftp_client import SFTPClient
from tqdm import tqdm

from akindness.device_agnostic_file_storage.remarkable.authentication import get_remarkable_password, \
    get_remarkable_ip_address
from akindness.device_agnostic_file_storage.util.graph.unique_multi_di_graph import UniqueMultiDiGraph

REMARKABLE_DOCUMENTS_PATH = "/home/root/.local/share/remarkable/xochitl/"


def explore(temp_dir: Path = Path.cwd() / "temp") -> MultiDiGraph:
    download_metadata(temp_dir)
    graph = assemble_file_system_graph(temp_dir)
    return graph


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
    for metadata_path in tqdm(metadata_path_collection, desc="Downloading metadata", unit="metadata"):
        temp_metadata_path = temp_dir / metadata_path.split("/")[-1]
        sftp.get(metadata_path, temp_metadata_path)


def _get_metadata_path_collection(sftp: SFTPClient) -> tuple[str, ...]:
    raw_document_path_collection = sftp.listdir_iter(REMARKABLE_DOCUMENTS_PATH)
    metadata_path_collection = [
        REMARKABLE_DOCUMENTS_PATH + raw_document_path.filename
        for raw_document_path in tqdm(raw_document_path_collection, desc="Listing documents", unit="document")
        if raw_document_path.filename.endswith(".metadata")
    ]
    return tuple(metadata_path_collection)


def assemble_file_system_graph(temp_dir: Path) -> MultiDiGraph:
    graph = UniqueMultiDiGraph()
    root = "root"
    graph.add_node(root, visibleName="root")
    graph.add_node("trash", visibleName="trash")
    for metadata_path in tqdm(temp_dir.iterdir(), desc="Assembling graph", unit="metadata"):
        if not metadata_path.is_file() or not (metadata_path.suffix == ".metadata"):
            continue
        current_id = metadata_path.stem
        graph.add_node(current_id)
    for metadata_path in temp_dir.iterdir():
        if not metadata_path.is_file() or not (metadata_path.suffix == ".metadata"):
            continue
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)
            if metadata.get("deleted"):
                continue
            parent_id: str = metadata.get("parent")
            current_id = metadata_path.stem
            metadata["id"] = current_id
            graph.add_node(current_id, **metadata)
            if parent_id.strip() == "":
                parent_id = root
            graph.add_edge(parent_id, current_id, type="child")
    return graph
