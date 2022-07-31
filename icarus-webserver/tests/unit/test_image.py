from webserver.domain import events
from webserver.domain.model import Image, ImageMetaData


def test_add_image_meta_data_to_image():
    image_uuid = "uuid-123"
    file_name = image_uuid + ".png"
    file_base_path = "/path/to/files"

    meta_data_1 = ImageMetaData(
        image_uuid=image_uuid, label="test-label-1", bx=10, by=20, w=10, h=30
    )
    meta_data_2 = ImageMetaData(
        image_uuid=image_uuid, label="test-label-2", bx=10, by=20, w=10, h=30
    )

    image = Image(uuid=image_uuid, file_name=file_name, file_base_path=file_base_path)

    image.meta_data.add(meta_data_1)
    image.meta_data.add(meta_data_2)

    assert meta_data_1 in image.meta_data
    assert meta_data_2 in image.meta_data


def test_initial_stored_value_is_false():
    image_uuid = "uuid-123"
    file_name = image_uuid + ".png"
    file_base_path = "/path/to/files"

    image = Image(uuid=image_uuid, file_name=file_name, file_base_path=file_base_path)

    assert image.stored is False


def test_set_stored_true_sets_stored_true():
    image_uuid = "uuid-123"
    file_name = image_uuid + ".png"
    file_base_path = "/path/to/files"

    image = Image(uuid=image_uuid, file_name=file_name, file_base_path=file_base_path)

    image.set_stored(True)

    assert image.stored is True


def test_set_stored_false_sets_stored_false():
    image_uuid = "uuid-123"
    file_name = image_uuid + ".png"
    file_base_path = "/path/to/files"

    image = Image(uuid=image_uuid, file_name=file_name, file_base_path=file_base_path)

    image.set_stored(True)
    image.set_stored(False)

    assert image.stored is False


def test_set_stored_true_raises_correct_event():
    image_uuid = "uuid-123"
    file_name = image_uuid + ".png"
    file_base_path = "/path/to/files"

    image = Image(uuid=image_uuid, file_name=file_name, file_base_path=file_base_path)
    image.set_stored(True)

    expected = events.StoredImageOnFileSystem(
        file_path=file_base_path + "/" + file_name
    )

    assert image.events[-1] == expected


def test_as_dict():
    image_uuid = "uuid-123"
    file_extension = "png"
    file_name = image_uuid + "." + file_extension
    file_base_path = "/path/to/files"

    image = Image(
        uuid=image_uuid,
        file_name=file_name,
        file_base_path=file_base_path,
        meta_data=set(),
    )

    expected = dict(
        uuid=image_uuid,
        file_name=file_name,
        file_path=file_base_path + "/" + file_name,
        file_extension=file_extension,
        stored=False,
        time_stamp=image.time_stamp,
        meta_data=[],
    )

    assert image.asdict() == expected
