import logging
import datetime
from . import domain

logger = logging.getLogger(__name__)


def _preserialize(input):
    output = None

    if isinstance(input, dict):
        output = dict()
        for key, value in input.items():
            value = _preserialize(value)
            output[key] = value
    elif isinstance(input, list):
        output = list()
        for element in input:
            output.append(_preserialize(element))
    elif isinstance(input, datetime.datetime):
        output = input.isoformat()
    else:
        output = input
    return output


def get_all_images(uow):
    with uow:
        results = uow.session.execute(
            """
                SELECT * FROM images
            """
        )

    return _preserialize([dict(r) for r in results])


def get_image_by_uuid(uuid, uow):
    with uow:
        result = uow.session.execute(
            """
                SELECT * FROM images WHERE uuid = :uuid
            """,
            dict(uuid=uuid),
        ).first()

    if not result:
        return

    return _preserialize(dict(result))
