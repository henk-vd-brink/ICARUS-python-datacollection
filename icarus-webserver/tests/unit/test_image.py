from webserver.domain import events
from webserver.domain.model import Image


def test_image_has_correct_attributes_after_instantiating():
    uuid = "test_uuid"
    file_name = "test_uuid.png"
    file_base_path = "/path/to/image"

    image = Image(uuid=uuid, file_name=file_name, file_base_path=file_base_path)

    assert image.uuid == uuid
    assert image.file_name == file_name
    assert image.file_path == "/path/to/image/test_uuid.png"
    assert image.file_extension == "png"
    assert image.stored is False
    assert isinstance(image.time_stamp, str)


def test_set_stored_true_sets_stored_true():
    uuid = "test_uuid"
    file_name = "test_uuid.png"
    file_base_path = "/path/to/image"

    image = Image(uuid=uuid, file_name=file_name, file_base_path=file_base_path)

    image.set_stored(True)

    assert image.stored is True


def test_set_stored_false_sets_stored_false():
    uuid = "test_uuid"
    file_name = "test_uuid.png"
    file_base_path = "/path/to/image"

    image = Image(uuid=uuid, file_name=file_name, file_base_path=file_base_path)

    image.set_stored(True)
    image.set_stored(False)

    assert image.stored is False


def test_set_stored_true_raises_correct_event():
    uuid = "test_uuid"
    file_name = "test_uuid.png"
    file_base_path = "/path/to/image"

    image = Image(uuid=uuid, file_name=file_name, file_base_path=file_base_path)
    image.set_stored(True)

    expected = events.StoredImageOnFileSystem(
        file_path=file_base_path + "/" + file_name
    )

    assert image.events[-1] == expected
