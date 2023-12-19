# Vector Search

## Commands
#### 1. Setup/reset external services
```
./dev.sh reset
```

#### 2. Start services
```
./dev.sh start
```
UI must be available at http://localhost:3000

#### 3. Run file scaner
```
./dev.sh scan
```
After a successful run, data would be available in the database.

#### 4. Stop services
```
./dev.sh stop
```

## Prerequisite

#### 1. Create a virtual environment and install pip dependencies
All the following commands must be run inside `./backend`
Ensure you have python 3.9.16
```
# Using virtualenv
pip install virtualenv
virtualenv venv
source venv/bin/activate

OR

# Using Conda
conda create --name vsenv python=3.9.16
conda activate vsenv
```

Install requirements
```
brew install ffmpeg
brew install libmagic
pip install -r requirements.txt
```

#### 2. Start external services
```
# Start PostgreSQL
docker run -p 5431:5432 --name vs-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres

# Start Elasticsearch
docker run --rm --detach -p 9200:9200 -p 9300:9300 -e "xpack.security.enabled=false" -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:8.7.0

# Start RabbitMQ
docker run -d -p 5672:5672 rabbitmq
```

#### 3. Load documents
```
Copy files into ./data directory
```

## Run Backend UTs
```
nosetests --nocapture

# To run specific test
nosetests --nocapture core/test_chunk.py:test_chunkify
```
