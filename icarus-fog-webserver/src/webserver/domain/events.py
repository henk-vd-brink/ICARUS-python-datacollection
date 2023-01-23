from dataclasses import dataclass


class Event:
    pass


@dataclass
class StoredUploadedImage(Event):
    uuid: str


@dataclass
class StoredImageMetaData(Event):
    uuid: str
