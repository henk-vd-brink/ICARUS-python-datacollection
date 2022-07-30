import os
from .adapters import mqtt_client as mqtt

def get_postgres_uri():
    host = os.environ.get("DB_IP_ADDRESS", "localhost")
    port = 54321 if host == "localhost" else 5432
    password = os.environ.get("DB_USER_PASSWORD", "abc123")
    user, db_name = "postgres", "postgres"
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

def get_host_mount_path():
    return os.environ.get("HOST_MOUNT_PATH", "/usr/docker_user/data")

def get_mqtt_config():
    return mqtt.MqttConfig(
        broker_ip_address=os.environ.get("MQTT_BROKER_IP_ADDRESS", "localhost"),
        broker_port=1883,
        broker_publish_topic=os.environ.get("MQTT_BROKER_PUBLISH_TOPIC", "/logs"),
        broker_subscribe_topics=["/events"]
    )