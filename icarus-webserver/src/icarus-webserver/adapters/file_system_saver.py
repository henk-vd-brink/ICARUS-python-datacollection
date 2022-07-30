import os
import logging

logger = logging.getLogger(__name__)

class FileSystemSaver:

    def __init__(self):
        self.base_path = "/usr/docker_user/data/"

    def save(self, file_name, bytes):
        try:
            self._save(
                file_name=file_name,
                bytes=bytes
                )
        except Exception as e:
            logger.info(str(e))

    def file_exists(self, file_name):
        return os.path.exists(self.base_path + file_name)

    def _save(self, file_name, bytes):
        with open(self.base_path + file_name, "wb") as f:
            f.write(bytes.read())