import json
import psycopg2
from kafka import KafkaConsumer
import logging
from kodama import config


logging.basicConfig(format=config.LOG_FORMAT, level=config.LOG_LEVEL)


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
    logging.info(f'Inserting: {data}')
    cur.execute(
        f"INSERT INTO checklog(url, response_time, return_code, regex_matches) "
        f"VALUES (\'{data['url']}\', {data['response_time']}, {data['return_code']}, {data['regex_matches']})"
    )


def consume(consumer, db):
    counter = 0
    for message in consumer:
        try:
            insert(db.cursor(), message.value)
            counter += 1
        except Exception as ex:
            logging.error("Unable to write to DB: %s", ex)
            db.rollback()
            logging.error("Transaction rollback.")
            counter = 0  # reset counter
        else:
            if config.DB_COMMIT:
                if counter >= config.DB_COMMIT_CHUNK:
                    logging.info("Commiting to DB.")
                    db.commit()
                    counter = 0  # reset counter
            else:
                logging.warning("Commiting to DB is disabled.")


if __name__ == '__main__':
    consumer = get_consumer()
    consume(consumer, get_db_connection())