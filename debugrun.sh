#!/bin/bash

docker-compose down
./build.sh

docker-compose up -d

docker-compose logs -f

