import logging
import dataclasses

from .. import config
from ..domain import model, commands, events

logger = logging.getLogger(__name__)

FILE_BASE_PATH = config.get_host_mount_path()


def create_image(cmd, uow):
    image_uuid = cmd.image_uuid
    meta_data = cmd.meta_data

    with uow:
        image = uow.images.get(uuid=image_uuid)

        if image is None:
            image = model.Image(
                uuid=image_uuid,
                file_name=None,
                file_base_path=FILE_BASE_PATH,
            )
            uow.images.add(image)

        for meta_data_element in meta_data:
            image_meta_data = model.ImageMetaData(
                image_uuid=image_uuid,
                label=meta_data_element.get("label"),
                bx=meta_data_element.get("bx"),
                by=meta_data_element.get("by"),
                w=meta_data_element.get("w"),
                h=meta_data_element.get("h"),
            )
            image.meta_data.add(image_meta_data)

        uow.commit()


def create_image_from_store_event(cmd, uow):
    image_uuid, file_extension = cmd.file_name.split(".")

    with uow:
        image = uow.images.get(uuid=image_uuid)

        if image is None:
            image = model.Image(
                uuid=image_uuid,
                file_name=None,
                file_base_path=FILE_BASE_PATH,
            )
            uow.images.add(image)

        image.set_file_information(
            file_base_path=FILE_BASE_PATH,
            file_name=cmd.file_name,
            file_extension=file_extension,
            stored=True,
        )

        uow.commit()


def add_meta_data_to_image(cmd, uow):
    image_uuid = cmd.image_uuid
    image_meta_data = cmd.meta_data

    if image_meta_data is None:
        return

    with uow:
        image = uow.images.get(uuid=image_uuid)

        if image is None:
            image = model.Image(
                uuid=image_uuid,
                file_name=None,
                file_base_path=FILE_BASE_PATH,
            )
            uow.images.add(image)

        while image_meta_data:
            meta_data = image_meta_data.pop()

            image.meta_data.add(
                model.ImageMetaData(
                    image_uuid=image_uuid,
                    label=meta_data.get("label"),
                    x_1=meta_data.get("x_1"),
                    y_1=meta_data.get("y_1"),
                    x_2=meta_data.get("x_2"),
                    y_2=meta_data.get("y_2"),
                    confidence=meta_data.get("confidence")
                )
            )

        uow.commit()


def log_event(event):
    logger.info(dataclasses.asdict(event))


COMMAND_HANDLERS = {
    commands.CreateImage: create_image,
    commands.AddMetaDataToImage: add_meta_data_to_image,
    commands.CreateImageFromStoreEvent: create_image_from_store_event,
}

EVENT_HANDLERS = {
    events.StoredImageOnFileSystem: [log_event],
    events.StoredImageMetaData: [log_event],
}
