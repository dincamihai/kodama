import asyncio
import pytest
from kodama import producer
from json import dumps
from mock import patch, Mock, MagicMock


@patch('kodama.producer.KafkaProducer')
def test_get_producer(mock_KafkaProducer):
    prod = producer.get_producer()
    assert prod == mock_KafkaProducer.return_value
    mock_KafkaProducer.assert_called_once_with(
        bootstrap_servers=['localhost:9092'],
        value_serializer=producer.value_serializer
    )


def test_produce():
    mock_producer = Mock()
    mock_producer.send.side_effect = [None, Exception]
    with pytest.raises(Exception):
        with patch('kodama.producer.asyncio', MagicMock()):
            asyncio.run(producer.produce(mock_producer))
    mock_producer.send.assert_called_once_with('testt', value={'number': 0})