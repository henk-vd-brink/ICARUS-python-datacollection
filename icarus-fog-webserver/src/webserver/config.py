import os


def get_postgres_uri():
    host = os.environ.get("DB_IP_ADDRESS", "localhost")
    port = 5432
    password = os.environ.get("DB_USER_PASSWORD", "abc123")
    user = os.environ.get("DB_USER_USERNAME", "postgres")
    db_name = os.environ.get("DB_NAME", "postgres")
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_host_mount_path():
    return os.environ.get("HOST_MOUNT_PATH", "/home/docker_user/data")


def get_container_base_path():
    return "/home/docker_user/data"


def get_rabbitmq_config():
    return dict(
        broker_ip_address="icarus-fog-rabbitmqbroker",
    )


def get_eventhub_config():
    return dict(
        eventhub_connection_string=os.environ.get("EVENTHUB_CONNECTION_STRING"),
        eventhub_name=os.environ.get("EVENTHUB_NAME"),
    )
