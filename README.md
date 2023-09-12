# Vector Search

### 1. Install pip dependencies
```
pip install tika numpy spacy psycopg2-binary
python -m spacy download en_core_web_lg
```

### 2. Start and setup database
2.a To start postgres in docker locally
```
docker run -p 5431:5432 --name vs-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres
```
2.b To setup the database
```
python db_migrate.py
```

### 3. Load documents
```
Copy PDFs into ./data-pdfs directory
```

### 4. Run extract pipeline
```
python extract_pipeline.py
```

After a successful run, data would be available in the database.
