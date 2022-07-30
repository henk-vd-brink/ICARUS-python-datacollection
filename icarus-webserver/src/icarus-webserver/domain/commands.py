import tempfile
from schema import Schema
from dataclasses import make_dataclass

class Command:
    pass

def command_factory(name, **fields):
    schema  = Schema(fields, ignore_extra_keys=True)
    cls = make_dataclass(name, fields.keys(), bases=(Command,)) 
    cls.from_dict = lambda s: cls(**schema.validate(s))
    return cls

StoreImageOnFileSystem = command_factory(
    "StoreImageOnFileSystem",
    image_bytes=tempfile.SpooledTemporaryFile,
    file_name=str
    )

StoreImageMetaData = command_factory(
    "StoreImageMetaData",
    file_name=str,
    meta_data=list
)