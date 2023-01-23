import os
import logging

logger = logging.getLogger(__name__)


class FileSaver:
    def __init__(self, base_path="/home/docker_user/data/"):
        self.base_path = base_path

    def save(self, file_name, file_bytes):
        try:
            self._save(file_name=file_name, file_bytes=file_bytes)
        except Exception as e:
            logger.info(str(e))

    def file_exists(self, file_name):
        return os.path.exists(self.base_path + file_name)

    def get_absolute_file_path(self, file_name):
        return self.base_path + file_name

    def _save(self, file_name, file_bytes):
        with open(self.base_path + file_name, "wb") as f:
            f.write(file_bytes.read())
