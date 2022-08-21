def store_image_on_file_system(cmd, uow):
    image_bytes = cmd.image_bytes
    file_name = cmd.file_name

    image_uuid, file_extension = file_name.split(".")

    with uow:
        image = uow.images.get(uuid=image_uuid)

        if image is None:
            image = model.Image(
                uuid=image_uuid,
                file_name=None,
                file_base_path=FILE_BASE_PATH,
            )
            uow.images.add(image)

        uow.files.add(file_name=file_name, bytes=image_bytes)

        if uow.files.file_exist(file_name=file_name):
            image.set_stored(stored=True)
            image.set_file_information(FILE_BASE_PATH, file_name, file_extension)

        uow.commit()
