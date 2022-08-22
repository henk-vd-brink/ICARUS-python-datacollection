import tempfile
from dataclasses import dataclass


class Command:
    pass


@dataclass(unsafe_hash=True)
class StoreFileOnFileSystem(Command):
    file_bytes: tempfile.SpooledTemporaryFile
    file_name: str
