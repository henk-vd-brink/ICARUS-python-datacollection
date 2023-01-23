import json


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
