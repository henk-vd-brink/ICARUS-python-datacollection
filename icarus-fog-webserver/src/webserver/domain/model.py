from dataclasses import dataclass, asdict
import datetime
import pathlib

from . import events


class Image:
    def __init__(self, uuid, file_name=None, file_path=None, meta_data=set()):
        self.uuid = uuid
        self.file_name = file_name
        self.file_path = file_path

        if file_path:
            self.file_extension = pathlib.Path(file_path).suffix

        self.stored = False
        self.timestamp = datetime.datetime.utcnow()
        self._meta_data = meta_data

        self.events = []

    def get_meta_data(self):
        return [asdict(m) for m in self._meta_data]

    def add_meta_data(self, meta_data):
        for meta_data_element in meta_data:
            self._meta_data.add(ImageMetaData.from_dict(meta_data_element))

        if meta_data:
            self.events.append(events.StoredImageMetaData(self.uuid))

    @classmethod
    def from_file_path(cls, file_path):
        file = pathlib.Path(file_path)

        uuid = file.stem
        file_name = file.name

        return cls(
            uuid=uuid,
            file_name=file_name,
            file_path=file_path,
        )

    def set_stored(self, stored):
        self.stored = stored

        if stored:
            self.events.append(events.StoredUploadedImage(self.uuid))


@dataclass(unsafe_hash=True)
class ImageMetaData:
    label: str
    x_1: float
    y_1: float
    x_2: float
    y_2: float
    confidence: float

    @classmethod
    def from_dict(cls, input_dict):
        return cls(
            label=input_dict["label"],
            x_1=input_dict["x_1"],
            y_1=input_dict["y_1"],
            x_2=input_dict["x_2"],
            y_2=input_dict["y_2"],
            confidence=input_dict["confidence"],
        )
