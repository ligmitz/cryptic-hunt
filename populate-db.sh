#!/bin/bash
cd "$(dirname "$0")"

WORKING_DIR="/opt/iste/abhedya"
cd $WORKING_DIR

cd docker
docker-compose up -d
docker-compose exec app python "manage.py" "loaddata" "questions/fixtures/questions.json"
docker-compose down
cd ..
