import asyncio
import aiohttp
from time import sleep
from json import dumps
from kafka import KafkaProducer
from kodama import config


def value_serializer(value):
    return dumps(value).encode('utf-8')


def get_producer():
    return KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=value_serializer
    )


async def fetch(session, url):
    async with session.get(url) as response:
        return (await response.text(), response.status)


async def produce(producer):
    loop = asyncio.get_event_loop()
    while True:
        for url in config.URLS:
            async with aiohttp.ClientSession() as session:
                resp, status = await fetch(session, url)
            value={
                'response_time': 0,
                'url': url,
                'response_code': status,
                'regex_matches': True
            }
            producer.send(config.KAFKA_TOPIC, value=value)


if __name__ == '__main__':
    producer = get_producer()
    asyncio.run(produce(producer))