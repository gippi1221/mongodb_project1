### to properly launch the docker-compose you have to create an .env file with the folowing variables
export DB_CONN=mongodb://<user>:<pass>@<mongodb-server>:27017/?authMechanism=DEFAULT<br>
export DB_NAME=sampleDB<br>
export TG_TOKEN=<your token ID from botfather><br>

to restore data from dump run the command below inside the docker container<br>
mongorestore /dump/sampleDB/sample_collection.bson -u <user> -p <pass>