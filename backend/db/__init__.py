from utils.logger import log

import os
from pathlib import Path

# TODO: Use SQLmodel instead of Psycopg2
from psycopg2 import connect
from psycopg2.extensions import connection

from utils.configs import db_configs

conn: connection

def get_conn() -> connection:
    return conn

def init():
    log.info("Establishing database connection")
    global conn
    conn = connect(db_configs.get_dsn())
    log.info('Database connection established')

def terminate():
   conn.close()

def migrate():
    schema = Path(os.getcwd()).joinpath('db/schema.sql').read_text()
    with conn.cursor() as cursor:
        cursor.execute(schema)
        conn.commit()
        return schema
