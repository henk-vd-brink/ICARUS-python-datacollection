def store_image_on_file_system(cmd, saver):
    image_bytes = cmd.image_bytes
    file_name = cmd.file_name

    saver.files.add(file_name=file_name, bytes=image_bytes)

    if saver.files.file_exist(file_name=file_name):
        print("joe")
