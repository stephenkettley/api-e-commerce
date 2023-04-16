import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

load_dotenv()

try:
    conn = psycopg2.connect(
        host="localhost",
        database="e-commerce",
        user=os.getenv("PG_USERNAME"),
        password=os.getenv("PG_PASSWORD"),
        cursor_factory=RealDictCursor,
    )
    cursor = conn.cursor()
    print("successfully connected to database")
except Exception as error:
    print("connection to database failed")
    print("Error: ", error)
