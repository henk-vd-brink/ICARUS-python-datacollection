import pytest

pytestmark = pytest.mark.usefixtures("mappers")


def insert_image(
    session, uuid, file_name, file_path, file_extension, stored, time_stamp
):

    session.execute(
        "INSERT INTO images (uuid, file_name, file_path, file_extension, stored, time_stamp) \
            VALUES (:uuid, :file_name, :file_path, :file_extension, :stored, :time_stamp)",
        dict(
            uuid=uuid,
            file_name=file_name,
            file_path=file_path,
            file_extension=file_extension,
            stored=stored,
            time_stamp=time_stamp,
        ),
    )


def get_image_uuid_by_image_uuid(session, uuid):
    [[uuid_]] = session.execute(
        "SELECT uuid \
            FROM images WHERE uuid=:uuid",
        dict(uuid=uuid),
    )
    return uuid_


def test_uow_can_retrieve_an_image(sqlite_session_factory):
    session = sqlite_session_factory()

    insert_image(
        session,
        "test-uuid1",
        "test-uuid1.png",
        "/path/to/test-uuid1.png",
        "png",
        True,
        "time_stamp",
    )
    session.commit()

    uuid = get_image_uuid_by_image_uuid(session, "test-uuid1")

    assert uuid == "test-uuid1"
