import abc
import os
import logging

logger = logging.getLogger(__name__)


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.session = None
        self.seen = set()


class FileSystemRepository(AbstractRepository):
    def __init__(self, base_path):
        super().__init__()
        self._base_path = base_path

    def add(self, file_name, bytes) -> None:
        try:
            self._save(file_name=file_name, bytes=bytes)
        except Exception as e:
            logger.info(str(e))
            raise e

    def file_exists(self, file_name):
        return os.path.exists(self._base_path + "/" + file_name)

    def _save_file(self, file_name, bytes) -> None:
        with open(self._base_path + "/" + file_name, "wb") as f:
            f.write(bytes.read())
