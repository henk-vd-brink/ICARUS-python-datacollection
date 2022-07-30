import os
import logging

from .. import config
from ..domain import model, commands, events

logger = logging.getLogger(__name__)

FILE_BASE_PATH = config.get_host_mount_path()

def store_image_meta_data(cmd, uow):
    file_name = cmd.file_name
    meta_data = cmd.meta_data

    image_uuid, _ = file_name.split(".")

    with uow:
        image = uow.images.get(uuid=image_uuid)

        if not image:
            image = model.Image(
                uuid = image_uuid,
                file_name = file_name,
                file_base_path = FILE_BASE_PATH,
            )
            uow.images.add(image)

        for meta_data_element in meta_data:
            image_meta_data = model.ImageMetaData(
                image_uuid = image_uuid,
                label = meta_data_element.get("label"),
                bx = meta_data_element.get("bx"),
                by = meta_data_element.get("by"),
                w = meta_data_element.get("w"),
                h = meta_data_element.get("h")
            )
            image.meta_data.add(image_meta_data)

        uow.commit()

def store_image_on_file_system(cmd, uow):
    image_bytes = cmd.image_bytes
    file_name = cmd.file_name

    image_uuid, _ = file_name.split(".")

    with uow:
        image = uow.images.get(uuid=image_uuid)

        if not image:
            image = model.Image(
                uuid = image_uuid,
                file_name = file_name,
                file_base_path = FILE_BASE_PATH,
            )
            uow.images.add(image)

        file_path = FILE_BASE_PATH + "/" + file_name
        image.file_path = file_path

        with open("/usr/docker_user/data/" + file_name, "wb") as f:
            f.write(image_bytes.read())

        image.set_stored(stored=True)
        uow.commit()
        

COMMAND_HANDLERS = {
    commands.StoreImageOnFileSystem: store_image_on_file_system,
    commands.StoreImageMetaData: store_image_meta_data,
}

EVENT_HANDLERS = {
    events.StoredImage: [],
    events.StoredImageMetaData: [],
}
