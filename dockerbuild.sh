#!/bin/bash

docker build -t "ingestion-api" --no-cache .
docker tag ingestion-api gcr.io/cidc-dfci/ingestion-api:dev
docker push gcr.io/cidc-dfci/ingestion-api:dev
