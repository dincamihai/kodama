import kodama
import psycopg2
from kodama import config

import pytest
from mock import patch, Mock


@pytest.fixture
def db():
    conn=psycopg2.connect(
        f"host='{config.DB_HOST}' dbname='{config.DB_NAME}' user='{config.DB_USER}' password='{config.DB_PASSWORD}'"
    )
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


@patch('kodama.consumer.config.DB_COMMIT', False)
def test_store(db, cur):
    data = {
        'response_time': 10,
        'url': 'http://yahoo.com',
        'response_code': 200,
        'regex_matches': True
    }
    kodama.consumer.store(db, data)
    cur.execute("SELECT COUNT(*) FROM checklog;")
    (result,) = cur.fetchone()
    assert result == 1