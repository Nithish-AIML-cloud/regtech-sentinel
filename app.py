import streamlit as st
import os
import psycopg2
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import google.generativeai as genai

st.set_page_config(page_title="RegTech Sentinel", page_icon="🏛️", layout="centered")

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

st.title("🏛️ RegTech Sentinel")
st.caption("AI-powered regulatory intelligence for RBI/SEBI circulars")

query = st.text_input("Ask a question about RBI circulars:", placeholder="e.g. What are the capital adequacy requirements for UCBs?")

if st.button("Ask") and query:
    with st.spinner("Searching circulars and generating answer..."):
        conn = psycopg2.connect(os.environ["NEON_DATABASE_URL"])
        cur = conn.cursor()

        query_embedding = model.encode(query).tolist()

        cur.execute("""
            SELECT source_file, chunk_text, embedding <=> %s::vector AS distance
            FROM chunks
            ORDER BY distance ASC
            LIMIT 5;
        """, (query_embedding,))

        results = cur.fetchall()

        context = ""
        for source_file, chunk_text, distance in results:
            context += f"[Source: {source_file}]\n{chunk_text}\n\n"

        prompt = f"""You are a regulatory compliance assistant for Indian banking (RBI/SEBI circulars).
Answer the question using ONLY the context provided below. If the context doesn't contain
enough information, say so clearly. Always cite which source document your answer comes from.

Context:
{context}

Question: {query}

Answer:"""

        gemini_model = genai.GenerativeModel("gemini-flash-latest")
        response = gemini_model.generate_content(prompt)

        cur.close()
        conn.close()

    st.markdown("### Answer")
    st.write(response.text)

    with st.expander("View retrieved source chunks"):
        for source_file, chunk_text, distance in results:
            st.markdown(f"**{source_file}** (distance: {distance:.4f})")
            st.text(chunk_text[:400])
            st.divider()