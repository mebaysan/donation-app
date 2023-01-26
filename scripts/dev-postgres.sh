#! /bin/bash

CONTAINER_NAME=ihya_database_dev

docker container run --name $CONTAINER_NAME -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -v ihya_database_dev:/var/lib/postgresql/data -d postgres