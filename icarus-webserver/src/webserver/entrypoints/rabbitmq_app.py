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
def stored_image_on_file_system_callback(ch, method, properties, parsed_message):
    try:
        bus.handle_message("CreateImageFromStoreEvent", parsed_message)
    except Exception as e:
        logger.exception(str(e))


CHANNEL_MAPPER = {"StoredImageOnFileSystem": stored_image_on_file_system_callback}


if __name__ == "__main__":
    broker_client.connect()

    for channel, call_back in CHANNEL_MAPPER.items():
        broker_client.channel.queue_declare(queue=channel)
        broker_client.channel.basic_consume(
            queue=channel,
            on_message_callback=call_back,
            auto_ack=True,
        )

    broker_client.channel.start_consuming()
