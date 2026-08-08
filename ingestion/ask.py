import os
import psycopg2
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env file
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to the database
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="regtech",
    user="postgres",
    password="regtech123"
)
cur = conn.cursor()

# The question
query = "What are the capital adequacy requirements for UCBs?"

# Step 1: Retrieve relevant chunks
query_embedding = model.encode(query).tolist()

cur.execute("""
    SELECT source_file, chunk_text, embedding <=> %s::vector AS distance
    FROM chunks
    ORDER BY distance ASC
    LIMIT 5;
""", (query_embedding,))

results = cur.fetchall()

# Step 2: Build context from retrieved chunks
context = ""
for source_file, chunk_text, distance in results:
    context += f"[Source: {source_file}]\n{chunk_text}\n\n"

# Step 3: Build the prompt
prompt = f"""You are a regulatory compliance assistant for Indian banking (RBI/SEBI circulars).
Answer the question using ONLY the context provided below. If the context doesn't contain
enough information, say so clearly. Always cite which source document your answer comes from.

Context:
{context}

Question: {query}

Answer:"""

# Step 4: Send to Gemini
gemini_model = genai.GenerativeModel("gemini-flash-latest")
response = gemini_model.generate_content(prompt)

print("Question:", query)
print("\nAnswer:\n")
print(response.text)

cur.close()
conn.close()