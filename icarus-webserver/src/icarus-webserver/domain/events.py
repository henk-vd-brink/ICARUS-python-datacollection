import json
from schema import And, Schema, Use
from dataclasses import dataclass, make_dataclass

class Event:
    pass

@dataclass
class StoredImageOnFileSystem(Event):
    file_path: str

@dataclass
class StoredImageMetaData(Event):
    pass
