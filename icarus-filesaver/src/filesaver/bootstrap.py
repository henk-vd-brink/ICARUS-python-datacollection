import inspect
import queue
import logging
from . import config

from .adapters import file_system_saver as fss
from .service_layer import handlers

logging.basicConfig(level=logging.INFO)


def bootstrap(file_system_saver=fss.FileSystemSaver()):

    dependencies = {"saver": file_system_saver}

    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    return {"command_handlers": injected_command_handlers}


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters

    deps = {
        name: dependency for name, dependency in dependencies.items() if name in params
    }
    return lambda message: handler(message, **deps)
