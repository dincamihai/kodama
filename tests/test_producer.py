import asyncio
import pytest
from kodama import producer
from json import dumps

from mock import patch, Mock, MagicMock
from aiohttp.test_utils import make_mocked_request

from aioresponses import aioresponses


@patch('kodama.producer.KafkaProducer')
def test_get_producer(mock_KafkaProducer):
    prod = producer.get_producer()
    assert prod == mock_KafkaProducer.return_value
    mock_KafkaProducer.assert_called_once_with(
        bootstrap_servers=['localhost:9092'],
        value_serializer=producer.value_serializer
    )


@pytest.mark.asyncio
async def test_produce():
    mock_producer = Mock()
    mock_producer.send.side_effect = [None, Exception]
    with pytest.raises(Exception):
        with aioresponses() as m:
            m.get('http://yahoo.com', status=200, body='htmlresp')
            await producer.produce(mock_producer)
    mock_producer.call_count = 2
    mock_producer.send.assert_called_with(
        'testt',
        value={
            'response_time': 0,
            'url': 'http://yahoo.com',
            'response_code': 200,
            'regex_matches': True
        }
    )