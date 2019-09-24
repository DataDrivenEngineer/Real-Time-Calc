#!/bin/sh

#echo "Updating and installing Docker"
sudo yum update -y
sudo yum upgrade -y
sudo yum install -y docker

#echo "Starting and enabling Docker"
sudo service docker start

echo "Configure database connection settings"
read -p "Postgres user name: " name
read -s -p "Postgres user password: " password
read -s -p "Postgres db name: " dbname
read -s -p "Postgres container name: " containername

export POSTGRES_USER=$name
export POSTGRES_PASSWORD=$password
export POSTGRES_DB=$dbname
export CONTAINER_NAME=$containername 

#sudo docker rm --force postgres || true

echo "Creating database container (and seed 'sample' database)"
sudo docker run -d \
  --name $CONTAINER_NAME \
  -e POSTGRES_USER=$POSTGRES_USER \
  -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
  -e POSTGRES_DB=$POSTGRES_DB \
  -p 80:5432 \
  --restart always \
  postgres:9.6.8-alpine
