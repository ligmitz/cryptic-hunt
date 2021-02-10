#!/bin/bash
WORKING_DIR="/opt/iste/abhedya"

if [ -d "$WORKING_DIR" ]; then
    echo "Removing Previous Installation";
    rm -Rf $WORKING_DIR;
fi

cp * $WORKING_DIR

echo "Copying the service file"
cp abhedya.service /etc/systemd/system/

echo "Enabeling the service"
systemctl enable abhedya.service

echo "Starting the service"
systemctl start abjedya.service

cd $WORKING_DIR

docker-compose up -d -f docker/docker-compose.yml
docker-compose exec app python manage.py questions/fixtures/questions.json
