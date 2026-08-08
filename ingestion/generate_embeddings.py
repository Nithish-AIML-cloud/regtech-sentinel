import json
import os
from sentence_transformers import SentenceTransformer

chunks_folder = "data/chunks"
embeddings_folder = "data/embeddings"

os.makedirs(embeddings_folder, exist_ok=True)

# Load the embedding model (downloads once, then cached)
print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded!")

chunk_files = [f for f in os.listdir(chunks_folder) if f.endswith(".json")]
print("Found chunk files:", chunk_files)

for filename in chunk_files:
    filepath = os.path.join(chunks_folder, filename)
    
    with open(filepath, "r", encoding="utf-8") as f:
        chunk_records = json.load(f)
    
    # Extract just the text from each chunk
    texts = [record["chunk_text"] for record in chunk_records]
    
    # Generate embeddings for all chunks in this file (batch processing)
    print(f"Generating embeddings for {filename} ({len(texts)} chunks)...")
    embeddings = model.encode(texts, show_progress_bar=True)
    
    # Attach the embedding vector to each chunk record
    for i, record in enumerate(chunk_records):
        record["embedding"] = embeddings[i].tolist()
    
    # Save to new file with embeddings included
    output_filename = filename.replace(".json", "_with_embeddings.json")
    output_path = os.path.join(embeddings_folder, output_filename)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunk_records, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {output_filename}")

print("Embedding generation done!")