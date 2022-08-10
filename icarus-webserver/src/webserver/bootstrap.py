import inspect
import queue
import logging
from . import config

from .adapters import (
    orm,
    mqtt_client as mqtt,
    file_system_saver as fss,
)

from .service_layer import messagebus, handlers, unit_of_work as uow

logging.basicConfig(level=logging.INFO)


def bootstrap(
    start_orm: bool = True,
    unit_of_work=uow.SqlAlchemyUnitOfWork(),
    saver=fss.FileSystemSaver(base_path="/usr/docker_user/data"),
):

    if start_orm:
        orm.start_mappers()

    mqtt_client = None

    dependencies = {"uow": unit_of_work, "saver": saver}

    injected_event_handlers = {
        event_type: [
            inject_dependencies(handler, dependencies) for handler in event_handlers
        ]
        for event_type, event_handlers in handlers.EVENT_HANDLERS.items()
    }

    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    return dict(
        bus=messagebus.MessageBus(
            command_handlers=injected_command_handlers,
            event_handlers=injected_event_handlers,
            uow=unit_of_work,
        ),
        mqtt_client=mqtt_client,
    )


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters

    deps = {
        name: dependency for name, dependency in dependencies.items() if name in params
    }
    return lambda message: handler(message, **deps)
