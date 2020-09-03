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

From lack of time I did not package it properly (as .deb and/or .rpm).