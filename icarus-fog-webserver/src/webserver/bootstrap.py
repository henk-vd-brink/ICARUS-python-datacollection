import inspect
import logging
from . import config

from .adapters import orm, rabbitmq_client as rbc, file_saver as fs

from .service_layer import messagebus, handlers, unit_of_work as uow

logging.basicConfig(level=logging.INFO)


def bootstrap(
    start_orm: bool = True,
    connect_to_rabbitmq_broker: bool = True,
    unit_of_work=uow.SqlAlchemyUnitOfWork(),
    rabbitmq_client=rbc.RabbitmqClient(config=config.get_rabbitmq_config()),
    file_saver=fs.FileSaver(),
):

    if start_orm:
        orm.start_mappers()

    if connect_to_rabbitmq_broker:
        rabbitmq_client.connect()

    dependencies = {
        "uow": unit_of_work,
        "file_saver": file_saver,
        "rabbitmq_client": rabbitmq_client,
    }

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
        broker_client=rabbitmq_client,
    )


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters

    deps = {
        name: dependency for name, dependency in dependencies.items() if name in params
    }
    return lambda message: handler(message, **deps)
