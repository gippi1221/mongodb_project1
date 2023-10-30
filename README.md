to properly launch the docker-compose you have to create an .env file with the folowing variables
export DB_CONN=mongodb://<user>:<pass>@localhost:27017/?authMechanism=DEFAULT
export DB_NAME=sampleDB
export TG_TOKEN=<your token ID from botfather>

to restore data from dump run the command below inside the docker container
mongorestore /dump/sampleDB/sample_collection.bson -u <user> -p <pass>