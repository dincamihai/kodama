import logging


BOOTSTRAP_SERVERS = ['localhost:9092']
DB_HOST = 'localhost'
DB_NAME = 'kodama'
DB_USER = 'kodama'
DB_PASSWORD = 'kodama'
DB_COMMIT = True
DB_COMMIT_CHUNK = 50
KAFKA_TOPIC = 'testt'
URLS = ('http://yahoo.com',)
LOG_FORMAT = '%(asctime)-15s - %(message)s'
LOG_LEVEL = logging.INFO