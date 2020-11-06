#!/bin/bash

docker-compose down
./build.sh
docker-compose run app mypy /code/

