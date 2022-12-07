import os


def get_postgres_uri():
    host = os.environ.get("DB_IP_ADDRESS", "localhost")
    port = 5432
    password = os.environ.get("DB_USER_PASSWORD", "abc123")
    user, db_name = os.environ.get("DB_USER_USERNAME", "postgres"), "postgres"
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_host_mount_path():
    return os.environ.get("HOST_MOUNT_PATH", "/home/docker_user/data")


def get_container_base_path():
    return "/home/docker_user/data"


def get_rabbitmq_config():
    return dict(
        broker_ip_address="icarus-fog-rabbitmqbroker",
    )
