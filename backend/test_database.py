import os
import psycopg
from dotenv import load_dotenv

load_dotenv()


try:
    connection = psycopg.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )

    print("✅ PostgreSQL connection successful!")

    connection.close()

except Exception as e:
    print("❌ PostgreSQL connection failed.")
    print(e)