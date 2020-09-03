#!/bin/bash
set -e

podman run \
	-p 5432:5432 \
	-v ./postgres/:/var/lib/postgresql/data:Z \
	-v ./docker-entrypoint-initdb.d/:/docker-entrypoint-initdb.d:Z \
	-e POSTGRES_DB=kodama \
	-e POSTGRES_USER=kodama \
	-e POSTGRES_PASSWORD=kodama \
	--net host \
	--name postgres \
	postgres
