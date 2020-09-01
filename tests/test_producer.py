import kodama
from mock import patch


@patch('kodama.producer.KafkaProducer')
def test_get_producer(mock_KafkaProducer):
    producer = kodama.producer.get_producer()
    assert producer == mock_KafkaProducer()