import logging
from . import domain

logger = logging.getLogger(__name__)


def get_all_images(uow):
    with uow:
        results = uow.session.execute(
            """
                SELECT * FROM images
            """
        )

    return [dict(r) for r in results]


def get_image_by_uuid(uuid, uow):
    with uow:
        result = (
            uow.session.query(domain.model.Image)
            .filter(domain.model.Image.uuid == uuid)
            .first()
        )
        uow.session.commit()

        if not result:
            return

        result_dict = result.asdict()

    return result_dict
