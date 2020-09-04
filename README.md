# kodama

The project uses kafka and postgres running in containers but `config.py` can be changed to connect to other instances.

#### Usage
```
pip install -r requirements-dev.txt
mkdir postgres/data
docker-compose up -d
python kodama/producer.py
python kodama/consumer.py
psql -h localhost -U kodama kodama -c "SELECT * FROM checklog;"
```

#### Testing
```bash
pytest
```


#### Notes

The OS distros packages should build here: https://build.opensuse.org/package/show/home:mihai.dinca/kodama [currently not building]

Most of the docker-compose file is borrowed from here: https://github.com/confluentinc/cp-all-in-one
