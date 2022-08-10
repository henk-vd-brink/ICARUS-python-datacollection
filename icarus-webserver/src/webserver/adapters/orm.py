import logging
from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    Date,
    Boolean,
    Float,
    ForeignKey,
    event,
)

from sqlalchemy.orm import mapper, relationship

from ..domain import model

logger = logging.getLogger(__name__)

metadata = MetaData()

images = Table(
    "images",
    metadata,
    Column("uuid", String, primary_key=True),
    Column("file_name", String, nullable=True),
    Column("file_path", String, nullable=True),
    Column("file_extension", String, nullable=True),
    Column("stored", Boolean, nullable=True),
    Column("time_stamp", String, nullable=False),
)

image_meta_data = Table(
    "image_meta_data",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("image_uuid", ForeignKey("images.uuid")),
    Column("label", String, nullable=True),
    Column("bx", Float, nullable=True),
    Column("by", Float, nullable=True),
    Column("w", Float, nullable=True),
    Column("h", Float, nullable=True),
)


def start_mappers():
    image_meta_data_mapper = mapper(model.ImageMetaData, image_meta_data)

    mapper(
        model.Image,
        images,
        properties={
            "_meta_data": relationship(image_meta_data_mapper, collection_class=set),
        },
    )


@event.listens_for(model.Image, "load")
def receive_load(image, _):
    image.events = []
