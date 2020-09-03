import asyncio
import aiohttp
import logging
import time
from json import dumps
from kafka import KafkaProducer
from kodama import config


logging.basicConfig(format=config.LOG_FORMAT, level=config.LOG_LEVEL)


def value_serializer(value):
    return dumps(value).encode('utf-8')


def get_producer():
    return KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=value_serializer
    )


async def fetch(session, url):
    start = time.time()
    response = await session.get(url)
    elapsed = time.time() - start
    return (await response.text(), response.status, elapsed)


async def produce(producer):
    loop = asyncio.get_event_loop()
    while True:
        for url in config.URLS:
            logging.info(f"Checking: {url}")
            async with aiohttp.ClientSession() as session:
                resp, status, elapsed = await fetch(session, url)
            value={
                'response_time': elapsed,
                'url': url,
                'return_code': status,
                'regex_matches': True
            }
            producer.send(config.KAFKA_TOPIC, value=value)


if __name__ == '__main__':
    producer = get_producer()
    asyncio.run(produce(producer))