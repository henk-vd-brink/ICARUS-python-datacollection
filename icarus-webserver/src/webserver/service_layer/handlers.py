import os
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


def add_meta_data_to_image(cmd, uow):
    image_uuid = cmd.image_uuid

    with uow:
        image = uow.images.get(uuid=image_uuid)

        if image is None:
            image = model.Image(
                uuid=image_uuid,
                file_name=None,
                file_base_path=FILE_BASE_PATH,
            )
            uow.images.add(image)

        image_meta_data = model.ImageMetaData(
            image_uuid=image_uuid,
            label=cmd.label,
            bx=cmd.bx,
            by=cmd.by,
            w=cmd.w,
            h=cmd.h,
        )

        image.meta_data.add(image_meta_data)
        uow.commit()


def log_event(event):
    logger.info(dataclasses.asdict(event))


COMMAND_HANDLERS = {
    commands.CreateImage: create_image,
    commands.AddMetaDataToImage: add_meta_data_to_image,
}

EVENT_HANDLERS = {
    events.StoredImageOnFileSystem: [log_event],
    events.StoredImageMetaData: [log_event],
}
