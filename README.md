# Vector Search

### 1. Install pip dependencies
```
pip install -r requirements.txt
```

### 2. Start and setup database
2.a To start postgres in docker locally
```
docker run -p 5431:5432 --name vs-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres
```
2.b To create tables and setup the database
```
python db_migrate.py
```

### 3. Load documents
```
Copy files into ./data directory
```

### 4. Run extract pipeline
```
python extract_pipeline.py
```
After a successful run, data would be available in the database.

### 5. Run UTs
```
nosetests --nocapture

# To run specific test
nosetests --nocapture core/test_chunk.py:test_chunkify
```

### 6. Start Server

```
uvicorn server:app --reload
```
