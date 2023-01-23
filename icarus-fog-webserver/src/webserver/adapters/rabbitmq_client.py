import pika
import logging


logger = logging.getLogger(__name__)


class RabbitmqClient:
    def __init__(self, config):
        self._config = config

        self._connection = None
        self._channel = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args, **kwargs):
        self._connection.close()

    def connect(self):
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(self._config.get("broker_ip_address"))
        )
        self._channel = self._connection.channel()

    def is_connected(self):
        if self._connection is None:
            return False

        return self._connection.is_open

    @property
    def channel(self):
        return self._channel
