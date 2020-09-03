import asyncio
import pytest
from kodama import producer
from json import dumps

from mock import patch, Mock, MagicMock, call
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
    mock_producer.send.call_count = 2
    assert mock_producer.send.mock_calls[0][1] == ('testt',)
    assert pytest.approx(mock_producer.send.mock_calls[0][2]['value']['response_time'], 0.01)
    assert mock_producer.send.mock_calls[0][2]['value']['url'] == 'http://yahoo.com'
    assert mock_producer.send.mock_calls[0][2]['value']['return_code'] == 200
    assert mock_producer.send.mock_calls[0][2]['value']['regex_matches'] is True