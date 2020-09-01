import kodama
from json import dumps
from mock import patch


@patch('kodama.producer.KafkaProducer')
def test_get_producer(mock_KafkaProducer):
    producer = kodama.producer.get_producer()
    assert producer == mock_KafkaProducer.return_value
    mock_KafkaProducer.assert_called_once_with(
        bootstrap_servers=['localhost:9092'],
        value_serializer=kodama.producer.value_serializer
    )