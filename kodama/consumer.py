import json
import psycopg2
from kafka import KafkaConsumer
import logging


def value_deserializer(value):
    return json.loads(value.decode('utf-8'))


def get_consumer():
    return KafkaConsumer(
        'testt',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='kodama',
        value_deserializer=value_deserializer
    )


def get_db_connection():
    try:
        conn=psycopg2.connect("host='localhost' dbname='kodama' user='kodama' password='kodama'")
        return conn
    except:
        logging.error("Unable to connect to DB.")


def insert(cur, data):
    cur.execute(f"INSERT INTO checklog VALUES ('{data['url']}', {data['response_time']}, {data['return_code']}, {data['regex_matches']})")


def store(conn, data, commit=False):
    try:
        insert(conn.cursor(), data)
    except:
        logging.error("Unable to write to DB.")
    else:
        if commit:
            conn.commit()
        else:
            logging.warning("Not commiting to DB.")


def consume(consumer, db):
    for message in consumer:
        message = message.value
        store(db, message, commit=True)


if __name__ == '__main__':
    consumer = get_consumer()
    consume(consumer, get_db_connection())