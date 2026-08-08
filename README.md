## Current Status

- ✅ End-to-end RAG pipeline (ingestion → retrieval → generation) working
- ✅ 399 chunks indexed across 5 real RBI Master Circulars
- ✅ Source-cited, context-grounded answers
- 🔜 Multi-agent orchestration (LangGraph)
- 🔜 LLM evaluation harness (golden dataset, LLM-as-judge)
- 🔜 FastAPI backend + Streamlit dashboard
- 🔜 LLMOps monitoring (drift detection)

## Setup

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start PostgreSQL + pgvector
docker run --name regtech-postgres -e POSTGRES_PASSWORD=regtech123 -e POSTGRES_DB=regtech -p 5432:5432 -d pgvector/pgvector:pg16

# Run the pipeline
python ingestion/extract_text.py
python ingestion/chunk_text.py
python ingestion/generate_embeddings.py
python ingestion/setup_database.py
python ingestion/insert_embeddings.py

# Ask a question
python ingestion/ask.py
```

## Author

Nithish R — [LinkedIn](https://linkedin.com/in/nithish-r-972588367) | [GitHub](https://github.com/Nithish-AIML-cloud)