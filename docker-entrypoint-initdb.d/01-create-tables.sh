#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
CREATE TABLE checklog (
    id INT GENERATED ALWAYS AS IDENTITY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    url VARCHAR NOT NULL,
    response_time INT NOT NULL,
    return_code INT NOT NULL,
    regex_matches BOOLEAN
)
EOSQL
