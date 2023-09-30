# Vector Search

## Backend
All the following commands must be run inside `./backend`

#### 1. Create a virtual environment and install pip dependencies
Ensure you have python 3.9.16
```
# With virtualenv
pip install virtualenv
virtualenv vs_env
source vs_env/bin/activate

#Conda
conda create --name vsenv python=3.9.16
conda activate vsenv

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

#### 3. Setup external services
```
python -m scripts.setup
```

#### 4. Load documents
```
Copy files into ./data directory
```

#### 5. Start services
Each command must be run in a seperate terminal
```
# Start Celery
celery -A tasks.extract worker --loglevel=INFO

# ReRank service
python -m services.rerank

# FAISS service
python -m services.vfaiss

# Start API server service
uvicorn services.api_server:app --reload
```

#### 6. Run file scaner
```
python -m scripts.file_scanner
```
After a successful run, data would be available in the database.

### Run Backend UTs
```
nosetests --nocapture

# To run specific test
nosetests --nocapture core/test_chunk.py:test_chunkify
```

## Frontend
All the following commands must be run inside `./frontend`

### 1. Start UI
```
npm start

# UI must be available at http://localhost:3000
```
