import os
import abc
import logging

logger = logging.getLogger(__name__)


class AbstractSaver(abc.ABC):

    def save_file(self, file_name, file_bytes) -> None:
        try:
            self._save_file(file_name=file_name, file_bytes=file_bytes)
        except Exception as e:
            logger.info(str(e))
            raise e

    @abc.abstractmethod
    def _save_file(self, file_name, file_bytes):
        pass

    @abc.abstractmethod
    def file_exists(self, file_name):
        pass


class FileSystemSaver(AbstractSaver):
    def __init__(self, base_path="/home/docker_user/data"):
        self._base_path = base_path

    def file_exists(self, file_name):
        return os.path.exists(self._base_path + "/" + file_name)

    def _save_file(self, file_name, file_bytes) -> None:
        with open(self._base_path + "/" + file_name, "wb") as f:
            f.write(file_bytes.read())
