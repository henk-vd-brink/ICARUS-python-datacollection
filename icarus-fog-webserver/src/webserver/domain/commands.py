import tempfile
from schema import Schema, And, Use, Or, Optional
from dataclasses import make_dataclass


def has_correct_file_extension(file_name):
    file_name_split = file_name.split(".")

    if len(file_name_split) == 1:
        return False

    return file_name.split(".")[1] in ["png", "jpg"]


class Command:
    pass


def command_factory(name, **fields):
    schema = Schema(fields, ignore_extra_keys=True)
    cls = make_dataclass(name, fields.keys(), bases=(Command,))
    cls.from_dict = lambda s: cls(**schema.validate(s))
    return cls


StoreUploadedImage = command_factory(
    "StoreUploadedImage",
    file_bytes=tempfile.SpooledTemporaryFile,
    file_name=And(Use(str), has_correct_file_extension),
)

CreateImage = command_factory(
    "CreateImage", uuid=str, file_path=str, meta_data=Or(None, list)
)

AddMetaDataToImage = command_factory(
    "AddMetaDataToImage", image_uuid=str, meta_data=list
)
