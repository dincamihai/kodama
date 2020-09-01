import kodama
from mock import patch


@patch('kodama.consumer.KafkaConsumer')
def test_get_producer(mock_KafkaConsumer):
    consumer = kodama.consumer.get_consumer()
    assert consumer == mock_KafkaConsumer()