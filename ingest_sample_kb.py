# This file is used to ingest the sample knowledge base into the pinecone index
# In simple words: it will take the sample knowledge base files,
# chunk them and add them to the pinecone index
# this script will run when we run the streamlit app for the first time
# or whenever the knowledge base is updated or chnaged.

from pathlib import Path
from app.core.config import get_settings
from app.services.ingestion import load_file, chunk_documents
from app.rag.vectorstore import add_documents

settings = get_settings()

folder = Path(settings.sample_kb_dir)
files = [p for p in folder.iterdir() if p.is_file()]

all_docs = []

for path in files:
    all_docs.extend(load_file(path))
chunks = chunk_documents(all_docs)
ids = add_documents(chunks)
print(f"Indexed {len(files)} files -> {len(chunks)} chunks -> {len(ids)} Pinecone vectors")