import logging
import json

from .. import bootstrap

logger = logging.getLogger(__name__)

bootstrap_items = bootstrap.bootstrap()

bus = bootstrap_items.get("bus")
broker_client = bootstrap_items.get("broker_client")


class ParseIncomingRabbitMqMessage:
    def __init__(self):
        pass

    def __call__(self, function):
        def wrapped(ch, method, properties, body):
            try:
                parsed_message = json.loads(body)
            except Exception:
                parsed_message = {}
            return function(ch, method, properties, parsed_message)

        return wrapped


@ParseIncomingRabbitMqMessage()
def callback(ch, method, properties, parsed_message):
    try:
        bus.handle_message("AddSegmentToTransaction", parsed_message)
    except Exception as e:
        logger.exception(str(e))


with broker_client:
    broker_client.connect()
    broker_client.channel.queue_declare(queue="hello-world")

    broker_client.channel.basic_consume(
        queue="hello-world",
        on_message_callback=callback,
        auto_ack=True,
    )

    broker_client.channel.start_consuming()
