import json
import datetime

from ..domain import commands

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def store_image_on_file_system(cmd, saver, rabbitmq_client):
    file_bytes = cmd.file_bytes
    file_name = cmd.file_name

    saver.add(file_name=file_name, bytes=file_bytes)

    if not saver.file_exists(file_name=file_name):
        return

    with rabbitmq_client:
        msg_as_dict = {
            "file_name": file_name,
            "time_stamp": datetime.datetime.now().strftime(DATETIME_FORMAT),
        }

        rabbitmq_client.send(
            routing_key="StoredImageOnFileSystem", body=json.dumps(msg_as_dict)
        )


COMMAND_HANDLERS = {commands.StoreFileOnFileSystem: store_image_on_file_system}
