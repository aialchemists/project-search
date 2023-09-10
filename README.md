# Vector Search

### Install Dependencies
```
pip install tika numpy spacy psycopg2-binary
python -m spacy download en_core_web_lg
```

### Start postgres database locally
```
docker run -p 5431:5432 --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres
```

### Prereqs
```
Copy PDFs into ./data-pdfs directory
```

### Run extract pipeline

```
python extract_pipeline.py
```

After a successful run, data would be available in the database.
