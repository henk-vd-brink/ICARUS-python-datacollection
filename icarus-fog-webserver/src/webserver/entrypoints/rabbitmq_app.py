import logging

from . import utils
from .. import bootstrap


logger = logging.getLogger(__name__)

bootstrap_items = bootstrap.bootstrap()

bus = bootstrap_items.get("bus")
broker_client = bootstrap_items.get("broker_client")


@utils.ParseIncomingRabbitMqMessage()
def stored_image_on_file_system_callback(ch, method, properties, parsed_message):
    try:
        bus.handle_message("CreateImage", parsed_message)
    except Exception as e:
        logger.exception(str(e))


@utils.ParseIncomingRabbitMqMessage()
def detected_objects_callback(ch, method, properties, parsed_message):
    try:
        bus.handle_message("AddMetaDataToImage", parsed_message)
    except Exception as e:
        logger.exception(str(e))


CHANNEL_MAPPER = {
    "StoredImageOnFileSystemQueue": {
        "exchange": "StoredImageOnFileSystem",
        "routing_key": "",
        "callback": stored_image_on_file_system_callback,
    },
    "DetectedObjectsQueue": {
        "exchange": "DetectedObjects",
        "routing_key": "jetson-nano0",
        "callback": detected_objects_callback,
    },
    "ImageInformationIsCompleteQueue": {
        "exchange": "ImageInformationIsComplete",
        "routing_key": "",
        "callback": None,
    },
}


if __name__ == "__main__":
    broker_client.connect()

    for queue, info in CHANNEL_MAPPER.items():
        exchange = info.get("exchange")
        routing_key = info.get("routing_key")
        callback = info.get("callback")

        if exchange:
            broker_client.channel.exchange_declare(
                exchange=exchange, exchange_type="direct"
            )
            logger.info("Declared exchange: %s", exchange)

        if not callback:
            continue

        broker_client.channel.queue_declare(queue=queue)

        broker_client.channel.queue_bind(
            queue=queue,
            exchange=exchange,
            routing_key=routing_key,
        )

        broker_client.channel.basic_consume(
            queue=queue,
            on_message_callback=callback,
            auto_ack=True,
        )

        logger.info("Connected to queue: %s", queue)

    broker_client.channel.start_consuming()
