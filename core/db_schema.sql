/**
file - Each row is a file that we have extracted
  - file_id       - Primary-key, Auto incrementing
  - file_path     - Stores the path to the file
  - metadata      - Metadata of the file in JSON format
*/
create table file (
  file_id SERIAL UNIQUE,
  file_path TEXT,
  metadata JSONB,

  CONSTRAINT unique_file_path UNIQUE (file_path)
);

/**
metadata - Each row is a KV pair of the selective file metadata
  - file_id + key - Primary-key
  - meta_key      - Metadata key
  - meta_value    - Value of metadata
*/
create table metadata (
  file_id INTEGER,
  meta_key VARCHAR(100),
  meta_value VARCHAR(256),

  PRIMARY KEY (file_id, meta_key),

  CONSTRAINT fk_file_id
    FOREIGN KEY(file_id)
    REFERENCES file(file_id)
);

/**
chunk - Each row is a chunk of text from the file. A file can be split into multiple parts/chunks. All chunks would be deleted and re-indexed if a file is modified
  - chunk_id       - Primary-key, Auto incrementing
  - file_id        - Foreign-key
  - chunk_text     - Part of the file represented by current chunk
  - embedding      - Embedding of the chunk_text (Need to investigate usage of pgvector: https://github.com/pgvector/pgvector)
  - start_position - Starting character position of the chunk in the file
*/
create table chunk (
  chunk_id SERIAL UNIQUE,
  file_id INTEGER,
  chunk_text TEXT,
  embedding float ARRAY,
  start_position INTEGER,
  length INTEGER,

  CONSTRAINT fk_file_id
    FOREIGN KEY(file_id)
    REFERENCES file(file_id)
);
