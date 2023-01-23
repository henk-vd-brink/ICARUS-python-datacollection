import pika
import time
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
        self._connection = self._connect()
        self._channel = self._connection.channel()

    def _connect(self):
        return pika.BlockingConnection(
            pika.ConnectionParameters(self._config.get("broker_ip_address"))
        )

    @property
    def channel(self):
        return self._channel
