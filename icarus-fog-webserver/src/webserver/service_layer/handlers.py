import logging
import json
import pathlib
import datetime

from .. import config
from ..domain import model, commands, events

logger = logging.getLogger(__name__)

FILE_BASE_PATH = config.get_host_mount_path()


def store_uploaded_image(cmd, file_saver, rabbitmq_client):
    file_name = cmd.file_name
    file_bytes = cmd.file_bytes

    uuid, _ = file_name.split(".")

    file_saver.save(file_name=file_name, file_bytes=file_bytes)

    if not file_saver.file_exists(file_name):
        logger.info("NOT STORED uploaded image on file_system.")
        return

    message_as_dict = {
        "uuid": uuid,
        "file_path": file_saver.get_absolute_file_path(file_name),
        "timestamp": datetime.datetime.now().isoformat(),
        "meta_data": None,
    }

    if not rabbitmq_client.is_connected():
        rabbitmq_client.connect()

    rabbitmq_client.channel.basic_publish(
        exchange="StoredImageOnFileSystem",
        routing_key="",
        body=json.dumps(message_as_dict),
    )

    logger.info("STORED uploaded image on file_system.")


def create_image(cmd, uow):
    uuid = cmd.uuid
    file_path = cmd.file_path

    with uow:
        image = uow.images.get(uuid=uuid)

        if image is None:
            image = model.Image.from_file_path(file_path)
            uow.images.add(image)
        else:
            image.file_name = pathlib.Path(file_path).name
            image.file_path = file_path

        image.set_stored(stored=True)

        uow.commit()

    logger.info("STORED image in database.")


def add_meta_data_to_image(cmd, uow):
    uuid = cmd.image_uuid
    meta_data = cmd.meta_data

    with uow:
        image = uow.images.get(uuid=uuid)

        if image is None:
            image = model.Image(uuid=uuid)
            uow.images.add(image)

        image.add_meta_data(meta_data)

        uow.commit()

    logger.info("STORED image meta data in database.")


def check_if_image_information_is_complete(event, uow, file_saver, rabbitmq_client):
    uuid = event.uuid

    with uow:
        image = uow.images.get(uuid=uuid)

        if image is None:
            return

        if image.file_path is None:
            return

        if not image.stored:
            return

        if not image._meta_data:
            return

        image_file_name = image.file_name
        meta_data = image.get_meta_data()

    message_as_dict = {
        "uuid": uuid,
        "file_name": image_file_name,
        "timestamp": datetime.datetime.now().isoformat(),
        "meta_data": meta_data,
    }

    if not rabbitmq_client.channel.is_open:
        rabbitmq_client.connect()

    rabbitmq_client.channel.basic_publish(
        exchange="ImageInformationIsComplete",
        routing_key="",
        body=json.dumps(message_as_dict),
    )

    logger.info("IMAGE INFORMATION IS COMPLETE")


COMMAND_HANDLERS = {
    commands.CreateImage: create_image,
    commands.AddMetaDataToImage: add_meta_data_to_image,
    commands.StoreUploadedImage: store_uploaded_image,
}

EVENT_HANDLERS = {
    events.StoredUploadedImage: [check_if_image_information_is_complete],
    events.StoredImageMetaData: [check_if_image_information_is_complete],
}
