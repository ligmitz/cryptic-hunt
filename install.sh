#!/bin/bash
cd "$(dirname "$0")"

WORKING_DIR="/opt/iste/abhedya"

if [ -d $WORKING_DIR ]; then
    echo "Found previous install. Stopping containers"
    cd $WORKING_DIR
    cd docker
    docker-compose down
fi

echo "Copying the service file"
cp abhedya.service /etc/systemd/system/

echo "Creating install dir"
mkdir -p $WORKING_DIR

cp -rf . -t $WORKING_DIR

cd $WORKING_DIR

echo "Enabling the service"
systemctl enable abhedya.service

cd docker
docker-compose build
cd ..

echo "Starting the service"
systemctl start abhedya.service


