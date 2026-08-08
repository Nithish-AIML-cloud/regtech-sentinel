import psycopg2
from sentence_transformers import SentenceTransformer

# Load the same embedding model used for the chunks
model = SentenceTransformer("all-MiniLM-L6-v2")

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="regtech",
    user="postgres",
    password="regtech123"
)

cur = conn.cursor()

# The question we want to search for
query = "What are the capital adequacy requirements for UCBs?"

# Convert the query into an embedding
query_embedding = model.encode(query).tolist()

# Search for the top 5 most similar chunks using cosine distance
cur.execute("""
    SELECT chunk_id, source_file, chunk_text, embedding <=> %s::vector AS distance
    FROM chunks
    ORDER BY distance ASC
    LIMIT 5;
""", (query_embedding,))

results = cur.fetchall()

print(f"Query: {query}\n")
print("Top 5 matching chunks:\n")

for i, (chunk_id, source_file, chunk_text, distance) in enumerate(results):
    print(f"--- Result {i+1} (distance: {distance:.4f}) ---")
    print(f"Source: {source_file}")
    print(f"Text: {chunk_text[:300]}")
    print()

cur.close()
conn.close()