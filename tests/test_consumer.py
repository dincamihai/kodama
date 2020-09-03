import kodama
import psycopg2

import pytest
from mock import patch, Mock


@pytest.fixture
def db():
    conn=psycopg2.connect("host='localhost' dbname='kodama' user='kodama' password='kodama'")
    return conn


@pytest.fixture
def cur(db):
    return db.cursor()


@patch('kodama.consumer.KafkaConsumer')
def test_get_consumer(mock_KafkaConsumer):
    consumer = kodama.consumer.get_consumer()
    assert consumer == mock_KafkaConsumer.return_value
    mock_KafkaConsumer.assert_called_once_with(
        'testt',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='kodama',
        value_deserializer=kodama.consumer.value_deserializer
    )


def test_store(db, cur):
    data = {
        'response_time': 10,
        'url': 'http://yahoo.com',
        'return_code': 200,
        'regex_matches': True
    }
    kodama.consumer.store(db, data)
    cur.execute("SELECT COUNT(*) FROM checklog;")
    (result,) = cur.fetchone()
    assert result == 1