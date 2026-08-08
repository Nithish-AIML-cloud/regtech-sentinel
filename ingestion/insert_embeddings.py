import json
import os
import psycopg2

embeddings_folder = "data/embeddings"

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="regtech",
    user="postgres",
    password="regtech123"
)

cur = conn.cursor()

embedding_files = [f for f in os.listdir(embeddings_folder) if f.endswith(".json")]
print("Found embedding files:", embedding_files)

total_inserted = 0

for filename in embedding_files:
    filepath = os.path.join(embeddings_folder, filename)
    
    with open(filepath, "r", encoding="utf-8") as f:
        chunk_records = json.load(f)
    
    for record in chunk_records:
        cur.execute("""
            INSERT INTO chunks (chunk_id, source_file, chunk_text, embedding)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (chunk_id) DO NOTHING;
        """, (
            record["chunk_id"],
            record["source_file"],
            record["chunk_text"],
            record["embedding"]
        ))
        total_inserted += 1
    
    print(f"Inserted chunks from {filename}")

conn.commit()
cur.close()
conn.close()

print(f"Done! Total chunks processed: {total_inserted}")