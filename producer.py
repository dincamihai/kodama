from time import sleep
from json import dumps
from kafka import KafkaProducer


def get_producer():
    return KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: dumps(x).encode('utf-8')
    )


def produce(producer):
    for e in range(1000):
        data = {'number' : e}
        producer.send('testt', value=data)
        sleep(5)


if __name__ == '__main__':
    producer = get_producer()
    produce(producer)