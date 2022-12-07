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

CreateImageFromStoreEvent = command_factory("CreateImageFromStoreEvent", file_name=str)

AddMetaDataToImage = command_factory(
    "AddMetaDataToImage", image_uuid=str, meta_data=list
)
