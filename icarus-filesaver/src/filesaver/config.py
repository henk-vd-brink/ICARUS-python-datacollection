import pathlib


def get_rabbitmq_config():
    return dict(broker_ip_address="icarus-rabbitmqbroker")


def get_base_file_path():
    return pathlib.Path("/home/docker_user/data")
