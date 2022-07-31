import json
import logging
import datetime

from .. import bootstrap
from ..domain import commands

logger = logging.getLogger(__name__)


class ParseIncomingMqttMessage:
    def __init__(self):
        pass

    def __call__(self, function):
        def wrapped(client, user_data, message):
            parsed_message = json.loads(message.payload)
            return function(client, user_data, parsed_message)

        return wrapped


def main():
    bootstrap_items = bootstrap.bootstrap()
    bus = bootstrap_items.get("bus")
    mqtt_client = bootstrap_items.get("mqtt_client")

    @ParseIncomingMqttMessage()
    def on_message(client, user_data, parsed_message):
        event_type = parsed_message.get("event_type")

        if event_type == "SentFileToServer":
            image_file_path = parsed_message.get("server_file_path")
            image_uuid = parsed_message.get("image_uuid")
            time_stamp = "time_stamp"

            cmd = commands.StoreImageMetaData(
                image_file_path=image_file_path,
                image_uuid=image_uuid,
                time_stamp=time_stamp,
            )

            bus.handle(cmd)
            logging.warning("RECEIVED CMD")
            logging.warning(cmd)

    mqtt_client.bind_on_message(on_message)
    mqtt_client.loop_forever()


if __name__ == "__main__":
    main()
