import asyncio
from time import sleep
from json import dumps
from kafka import KafkaProducer


def value_serializer(value):
    return dumps(value).encode('utf-8')


def get_producer():
    return KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=value_serializer
    )


async def produce(producer):
    for e in range(1000):
        data = {'number' : e}
        producer.send('testt', value=data)
        await asyncio.sleep(5)


if __name__ == '__main__':
    producer = get_producer()
    asyncio.run(produce(producer))