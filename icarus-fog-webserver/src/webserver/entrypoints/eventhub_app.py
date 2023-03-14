import logging
from azure.eventhub import EventHubConsumerClient

from .. import bootstrap, config

logger = logging.getLogger(__name__)

bootstrap_items = bootstrap.bootstrap()

bus = bootstrap_items.get("bus")

eventhub_config = config.get_eventhub_config()

CONNECTION_STRING = eventhub_config.get("eventhub_connection_string")
EVENTHUB_NAME = eventhub_config.get("eventhub_name")


def on_event(_, event):
    try:
        bus.handle_message("AddMetaDataToImage", event.body_as_json())
    except Exception as e:
        logger.exception(str(e))


def on_partition_initialize(partition_context):
    # Put your code here.
    print("Partition: {} has been initialized.".format(partition_context.partition_id))


def on_partition_close(partition_context, reason):
    # Put your code here.
    print(
        "Partition: {} has been closed, reason for closing: {}.".format(
            partition_context.partition_id, reason
        )
    )


def on_error(partition_context, error):
    # Put your code here. partition_context can be None in the on_error callback.
    if partition_context:
        print(
            "An exception: {} occurred during receiving from Partition: {}.".format(
                partition_context.partition_id, error
            )
        )
    else:
        print(
            "An exception: {} occurred during the load balance process.".format(error)
        )


if __name__ == "__main__":
    client = EventHubConsumerClient.from_connection_string(
        conn_str=CONNECTION_STRING,
        consumer_group="$Default",
        eventhub_name=EVENTHUB_NAME,
    )
    try:
        with client:
            client.receive(
                on_event=on_event,
                on_partition_initialize=on_partition_initialize,
                on_partition_close=on_partition_close,
                on_error=on_error,
                starting_position="-1",  # "-1" is from the beginning of the partition.
            )
    except KeyboardInterrupt:
        print("Receiving has stopped.")
