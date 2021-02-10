#!/bin/bash
cd "$(dirname "$0")"

WORKING_DIR="/opt/iste/abhedya"

cp -rf . -t $WORKING_DIR

echo "Copying the service file"
cp abhedya.service /etc/systemd/system/

cd $WORKING_DIR
docker-compose up -d -f docker/docker-compose.yml
docker-compose exec app python manage.py questions/fixtures/questions.json
docker-compose down

echo "Enabling the service"
systemctl enable abhedya.service

echo "Starting the service"
systemctl start abjedya.service


