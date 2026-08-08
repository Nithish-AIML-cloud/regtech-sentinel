import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="regtech",
    user="postgres",
    password="regtech123"
)

cur = conn.cursor()

# Enable the pgvector extension
cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
print("pgvector extension enabled!")

# Create the chunks table
cur.execute("""
    CREATE TABLE IF NOT EXISTS chunks (
        id SERIAL PRIMARY KEY,
        chunk_id TEXT UNIQUE,
        source_file TEXT,
        chunk_text TEXT,
        embedding VECTOR(384)
    );
""")
print("Table 'chunks' created!")

# Commit changes and close connection
conn.commit()
cur.close()
conn.close()

print("Database setup done!")