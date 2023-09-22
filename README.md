# Vector Search

## Backend
All the following commands must be run inside `./backend`

### 1. Create a virtual environment and install pip dependencies
Ensure you have python 3.9.16
```
pip install virtualenv
virtualenv vs_env
source vs_env/bin/activate

pip install -r requirements.txt
```

### 2. Start and setup database
2.a To start postgres in docker locally
```
docker run -p 5431:5432 --name vs-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres
```
2.b To create tables and setup the database
```
python -m services.migrate
```

### 3. Load documents
```
Copy files into ./data directory
```

### 4. ElasticSearch
Docker command to setup the server

```
 run --rm --detach -p 9200:9200 -p 9300:9300 -e "xpack.security.enabled=false" -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:8.7.0
```

### 5. Run extract pipeline
```
python extract_pipeline.py
```
After a successful run, data would be available in the database.

### 6. Run UTs
```
nosetests --nocapture

# To run specific test
nosetests --nocapture core/test_chunk.py:test_chunkify
```

### 7. Start services
#### ReRank service
```
python -m services.rerank
```

### 8. Start Server
```
uvicorn services.api_server:app --reload
```

## Frontend
All the following commands must be run inside `./frontend`

### 1. Start UI
```
npm start

UI must be available at http://localhost:3000
```
