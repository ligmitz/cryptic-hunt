#!/bin/bash
cd "$(dirname "$0")"

WORKING_DIR="/opt/iste/abhedya"
DOCKER_COMPOSE_PATH="$WORKING_DIR/docker/docker-compose.yml"
PATH="/usr/local/bin:$PATH"

if [ -d $WORKING_DIR ]; then
    echo "Found previous install. Stopping containers"
    docker-compose -f ${DOCKER_COMPOSE_PATH} down
fi

echo "Copying the service file"
cp abhedya.service /etc/systemd/system/

echo "Creating install dir"
mkdir -p $WORKING_DIR

rsync -av --progress . $WORKING_DIR/ --exclude .git --exclude venv

cd $WORKING_DIR

./gen-dhparams

echo "Enabling the service"
systemctl enable abhedya.service

cd docker
docker-compose build
cd ..

echo "Starting the service"
systemctl start abhedya.service


