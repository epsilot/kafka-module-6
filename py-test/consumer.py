import os
from confluent_kafka import Consumer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONDeserializer

if __name__ == "__main__":
    consumer_conf = {
        "bootstrap.servers": os.getenv('BOOTSTRAP_SERVER', ''),
        "group.id": "group-1",
        "auto.offset.reset": "earliest",
        "security.protocol": "SASL_SSL",

        # Настройки SASL-аутентификации
        "sasl.mechanism": "PLAIN",
        "sasl.username": "user",
        "sasl.password": os.getenv('PWD', ''),

        # Настройки TLS
        "ssl.ca.location": "ca.pem",
    }

    topic = "topic1"

    registry_config = {
        "url": os.getenv('SCHEMA_REGISTRY', ''),
        "basic.auth.user.info": f"user:{os.getenv('PWD', '')}",
        "ssl.ca.location": "ca.pem",
    }

    schema_registry_client = SchemaRegistryClient(registry_config)
    latest = schema_registry_client.get_latest_version(f'{topic}-value')

    json_deserializer = JSONDeserializer(latest.schema.schema_str, from_dict=lambda u, ctx: u)

    print(f"Читаем топик: {topic}")
    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])

    try:
        while True:
            message = consumer.poll(1.0)
            if message is None:
                continue
            if message.error():
                print(f"Ошибка: {message.error()}")
                continue

            context = SerializationContext(message.topic(), MessageField.VALUE)
            user = json_deserializer(message.value(), context)

            key = message.key().decode("utf-8")
            print(f"Получено сообщение: {key=}, {user=}, offset={message.offset()}")
    finally:
        consumer.close()
