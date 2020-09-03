import json
import psycopg2
from kafka import KafkaConsumer
import logging
from kodama import config


def value_deserializer(value):
    return json.loads(value.decode('utf-8'))


def get_consumer():
    return KafkaConsumer(
        config.KAFKA_TOPIC,
        bootstrap_servers=config.BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='kodama',
        value_deserializer=value_deserializer
    )


def get_db_connection():
    try:
        conn=psycopg2.connect(
            f"host='{config.DB_HOST}' dbname='{config.DB_NAME}' user='{config.DB_USER}' password='{config.DB_PASSWORD}'"
        )
        return conn
    except:
        logging.error("Unable to connect to DB.")


def insert(cur, data):
    cur.execute(f"INSERT INTO checklog VALUES (\'{data['url']}\', {data['response_time']}, {data['response_code']}, {data['regex_matches']})")


def store(conn, data):
    try:
        insert(conn.cursor(), data)
    except Exception as ex:
        logging.error(ex)
        logging.error("Unable to write to DB.")
    else:
        if config.DB_COMMIT:
            conn.commit()
        else:
            logging.warning("Not commiting to DB.")


def consume(consumer, db):
    for message in consumer:
        message = message.value
        store(db, message)


if __name__ == '__main__':
    consumer = get_consumer()
    consume(consumer, get_db_connection())