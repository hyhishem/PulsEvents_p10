import pandas as pd
import os
from dotenv import load_dotenv

from langchain_mistralai import MistralAIEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

# charger env
load_dotenv()   

# Chunk
CHUNK_SIZE = 600    
CHUNK_OVERLAP = 100


df = pd.read_parquet(os.getenv("DATA_PATH"))

text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len, # Important: mesure en caractères
        add_start_index=True # Ajoute la position de début du chunk dans le document original
)


documents = []
for _, row in df.iterrows():
    text=row["text_pour_embeding"]
    chunks = text_splitter.split_text(text)

    for i, chunk in enumerate(chunks):
        doc = Document(
            page_content=chunk,  
            metadata={
                "uid": row.get("uid"),
                "title": row.get("title_fr", ""),
                "chunk_index": i,
                "total_chunks": len(chunks),
                "url": row.get("canonicalurl", ""),
                "date_begin": str(row.get("firstdate_begin") or ""),
                "date_end": str(row.get("firstdate_end") or ""),
                "location_name": row.get("location_name", ""),
                "location_address": row.get("location_address", ""),
                "location_postalcode": row.get("location_postalcode", ""),
                "location_department": row.get("location_department", ""),
                "location_city": row.get("location_city", ""),       
            }
        )
        documents.append(doc)


embeddings = MistralAIEmbeddings(
    model=os.getenv("EMBEDDING_MODEL"),
    api_key=os.getenv("MISTRAL_API_KEY")
)


vector_db = FAISS.from_documents(
    documents=documents,
    embedding=embeddings
)

vector_db.save_local(os.getenv("VECTOR_DB_PATH"))

