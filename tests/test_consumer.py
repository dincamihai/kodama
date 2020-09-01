import kodama
from mock import patch


@patch('kodama.consumer.KafkaConsumer')
def test_get_consumer(mock_KafkaConsumer):
    consumer = kodama.consumer.get_consumer()
    assert consumer == mock_KafkaConsumer.return_value
    mock_KafkaConsumer.assert_called_once_with(
        'testt',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=kodama.consumer.value_deserializer
    )