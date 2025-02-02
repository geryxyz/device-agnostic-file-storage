import shutil
from pathlib import Path

from paramiko.client import SSHClient

from akindness.device_agnostic_file_storage.remarkable.authentication import get_remarkable_password, \
    get_remarkable_ip_address


REMARKABLE_DOCUMENTS_PATH = "/home/root/.local/share/remarkable/xochitl/"


def explore(temp_dir: Path = Path.cwd() / "temp"):
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
