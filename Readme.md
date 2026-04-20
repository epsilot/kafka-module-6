Apache Kafka для разработки и архитектуры

# Модуль 6. Kafka в production и интеграция Kafka с Big Data экосистемой

## Задание 1.Развёртывание и настройка Kafka-кластера в Yandex Cloud

### Шаг 1. Разворачивание и настройка кластера Kafka

1. Создан каталог для кластера

   ![1.1.png](img/1.1.png)

2. Выданы права доступа

   ![1.2.png](img/1.2.png)

3. Создан кластер. Комбинированный Kraft. Реестр схем данных. Открытый публичный доступ

   ![1.3.png](img/1.3.png)
   ![1.4.png](img/1.4.png)
   ![1.5.png](img/1.5.png)

4. Создан пользователь для чтения/записи созданного топика
   ![1.6.png](img/1.6.png)

### Шаг 2. Настройте репликацию и хранение данных

Создан топик с 3 партициями и фактором репликации 3.
- log.cleanup.policy = delete
- log.retention.ms = 8640000
- log.segment.bytes = 268435456

  ![2.1.png](img/2.1.png)
  ![2.2.png](img/2.2.png)

### Шаг 3. Настройте Schema Registry

Создана схема данных

```shell

curl -u "user:12345678" -X POST -k -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  --data '{
    "schemaType": "JSON",
    "schema": "{\"$schema\":\"http://json-schema.org/draft-07/schema#\",\"title\":\"User\",\"type\":\"object\",\"properties\":{\"name\":{\"type\":\"string\"},\"email\":{\"type\":\"string\"},\"age\":{\"type\":\"integer\"}},\"required\":[\"name\",\"email\"]}"
  }' \
  https://rc1a-7t10rr3kj4vqej4u.mdb.yandexcloud.net/subjects/topic1-value/versions

{"id":1}

```

### Шаг 4. Проверьте работу Kafka.

1. Генерируем сообщение в топик

```shell
sudo docker compose run producer 
/usr/local/lib/python3.13/site-packages/authlib/_joserfc_helpers.py:8: AuthlibDeprecationWarning: authlib.jose module is deprecated, please use joserfc instead.
It will be compatible before version 2.0.0.
  from authlib.jose import ECKey
Сообщение: key='key-239f892d-3fa6-4b2f-bd80-6cf0e258fc00', user={'name': 'IsiLWnzodt', 'email': 'XwoEKEFV@yandex.ru'} отправлено в топик: topic1
```

![4.1.png](img/4.1.png)

2. Читаем сообщение из топика

```shell
sudo docker compose run consumer  
/usr/local/lib/python3.13/site-packages/authlib/_joserfc_helpers.py:8: AuthlibDeprecationWarning: authlib.jose module is deprecated, please use joserfc instead.
It will be compatible before version 2.0.0.
  from authlib.jose import ECKey
Читаем топик: topic1
Получено сообщение: key='key-239f892d-3fa6-4b2f-bd80-6cf0e258fc00', user={'name': 'IsiLWnzodt', 'email': 'XwoEKEFV@yandex.ru'}, offset=0
```

