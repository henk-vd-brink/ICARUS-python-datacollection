import tempfile
from schema import Schema
from dataclasses import make_dataclass


class Command:
    pass


def command_factory(name, **fields):
    schema = Schema(fields, ignore_extra_keys=True)
    cls = make_dataclass(name, fields.keys(), bases=(Command,))
    cls.from_dict = lambda s: cls(**schema.validate(s))
    return cls


CreateImage = command_factory("CreateImage", image_uuid=str, meta_data=list)

AddMetaDataToImage = command_factory(
    "AddMetaDataToImage",
    image_uuid=str,
    label=str,
    bx=float,
    by=float,
    w=float,
    h=float,
)


StoreImage = command_factory(
    "StoreImage", image_bytes=tempfile.SpooledTemporaryFile, file_name=str
)
