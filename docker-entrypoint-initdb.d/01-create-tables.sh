#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
CREATE TABLE checklog (
    url text,
    response_time int,
    return_code int,
    regex_matches boolean
)
EOSQL
