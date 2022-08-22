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
        self._rollback()

    def connect(self, sleep_time=1, number_of_retries=10):
        for i in range(number_of_retries):
            try:
                self._connection = self._connect()
                self._channel = self._connection.channel()
                break
            except pika.exceptions.AMQPConnectionError:
                logger.warning(
                    f"Could not connect to broker, try again in {sleep_time} seconds.."
                )
                time.sleep(sleep_time + i)
        else:
            raise pika.exceptions.AMQPConnectionError

    def send(self, routing_key: str, body: str):
        self._channel.basic_publish(exchange="", routing_key=routing_key, body=body)

    def _connect(self):
        return pika.BlockingConnection(
            pika.ConnectionParameters(self._config.get("broker_ip_address"))
        )

    @property
    def channel(self):
        return self._channel

    def _rollback(self):
        try:
            self._connection.close()
        except Exception:
            pass
