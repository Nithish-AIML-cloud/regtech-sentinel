import json
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

processed_folder = "data/processed"
chunks_folder = "data/chunks"

os.makedirs(chunks_folder, exist_ok=True)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

json_files = [f for f in os.listdir(processed_folder) if f.endswith(".json")]
print("Found JSON files:", json_files)

for filename in json_files:
    filepath = os.path.join(processed_folder, filename)
    
    with open(filepath, "r", encoding="utf-8") as f:
        doc_data = json.load(f)
    
    text = doc_data["text"]
    chunks = splitter.split_text(text)
    
    print(f"{filename}: split into {len(chunks)} chunks")
    
    chunk_records = []
    for i, chunk in enumerate(chunks):
        chunk_records.append({
            "chunk_id": f"{filename.replace('.json', '')}_chunk_{i}",
            "source_file": doc_data["filename"],
            "chunk_text": chunk
        })
    
    output_filename = filename.replace(".json", "_chunks.json")
    output_path = os.path.join(chunks_folder, output_filename)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunk_records, f, ensure_ascii=False, indent=2)

print("Chunking done!")