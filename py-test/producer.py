import uuid
import random
import string
import os
from confluent_kafka import Producer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer


if __name__ == "__main__":
    config = {
        "bootstrap.servers": os.getenv('BOOTSTRAP_SERVER', ''),
        "security.protocol": "SASL_SSL",

        # Настройки SASL-аутентификации
        "sasl.mechanism": "PLAIN",
        "sasl.username": "user",
        "sasl.password": os.getenv('PWD', ''),

        # Настройка TLS
        "ssl.ca.location": "ca.pem",
    }

    registry_config = {
        "url": os.getenv('SCHEMA_REGISTRY', ''),
        "basic.auth.user.info": f"user:{os.getenv('PWD', '')}",
        "ssl.ca.location": "ca.pem",
    }
    topic = 'topic1'

    producer = Producer(config)

    schema_registry_client = SchemaRegistryClient(registry_config)
    latest = schema_registry_client.get_latest_version(f'{topic}-value')

    json_serializer = JSONSerializer(latest.schema.schema_str, schema_registry_client, lambda u, ctx: u)
    context = SerializationContext(topic, MessageField.VALUE)

    key = f"key-{uuid.uuid4()}"
    random_string = ''.join(random.choices(string.ascii_letters, k=random.randint(5, 10)))
    email = f"{random_string}@yandex.ru"
    name = ''.join(random.choices(string.ascii_letters, k=random.randint(5, 10)))
    user = {"name": name, "email": email}
    serialized_value = json_serializer(user, context)

    producer.produce(topic, key=key, value=serialized_value)
    producer.flush()

    print(f"Сообщение: {key=}, {user=} отправлено в топик: {topic}")
