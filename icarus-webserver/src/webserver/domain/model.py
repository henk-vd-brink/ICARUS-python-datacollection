from dataclasses import dataclass, asdict

from . import events


class Image:
    def __init__(self, uuid, file_name, file_base_path, meta_data=set()):
        self.uuid = uuid
        self.file_name = file_name
        self.file_path = self._get_file_path(file_base_path, file_name)
        self.file_extension = self._get_file_extension(file_name)
        self.stored = False
        self.time_stamp = self._get_time_stamp()
        self._meta_data = meta_data

        self.events = []

    def _get_time_stamp(self):
        return "time_stamp"

    def _get_file_path(self, file_base_path, file_name):
        if file_base_path and file_name:
            return file_base_path + "/" + file_name
        return ""

    def set_file_information(self, file_base_path, file_name, file_extension):
        self.file_name = file_name
        self.file_path = self._get_file_path(file_base_path, file_name)
        self.file_extension = file_extension

    def _get_file_extension(self, file_name):
        if file_name:
            return file_name.split(".")[-1]
        return ""

    @property
    def meta_data(self):
        return self._meta_data

    def set_stored(self, stored):
        self.stored = stored

        if not stored:
            return

        self.events.append(events.StoredImageOnFileSystem(file_path=self.file_path))

    def asdict(self):
        return dict(
            uuid=self.uuid,
            file_name=self.file_name,
            file_path=self.file_path,
            file_extension=self.file_extension,
            stored=self.stored,
            time_stamp=self.time_stamp,
            meta_data=[asdict(m) for m in self._meta_data],
        )


@dataclass(unsafe_hash=True)
class ImageMetaData:
    image_uuid: str
    label: str
    bx: float
    by: float
    w: float
    h: float
