/**
files
  - id - string
  - file_path - string
  - metadata - JSONB
*/
create table files(
	id VARCHAR(1024),
	file_path TEXT,
	metadata JSONB,

	PRIMARY KEY (id)
);

/**
chunks
  - id - int
  - file_id - int
  - chunk_text - string
  - embedding - float ARRAY (Need to investigate pgvector: https://github.com/pgvector/pgvector)
  - start_position - int
  - length - int
*/
create table chunks(
	id SERIAL,
	file_id VARCHAR(1024),
	chunk_text TEXT,
	embedding float ARRAY,
	start_position int,
	length int,

	PRIMARY KEY (id),
	CONSTRAINT fk_file
		FOREIGN KEY(file_id)
		REFERENCES files(id)
);
