from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS


#  Config 
load_dotenv()

VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")


# BDD 
def load_vector_db():
    embeddings = MistralAIEmbeddings(
        model=EMBEDDING_MODEL,
        api_key=MISTRAL_API_KEY
    )

    return FAISS.load_local(
        folder_path=VECTOR_DB_PATH,
        embeddings=embeddings,
        allow_dangerous_deserialization=True
    )


#  TEST 

vector_db = load_vector_db()

# récupération de tous les documents
docs = list(vector_db.docstore._dict.values())
assert len(docs) > 0, "La base est vide"

departements = set()
dates = []

for doc in docs:
    metadata = doc.metadata

    # TEST LOCALISATION 
    location_department = metadata.get("location_department", "").lower()
    assert location_department, f"Ville manquante dans doc : {doc}"
    
    departements.add(location_department)
    assert "essonne" in location_department, \
        f"Ville hors Essonne : {location_department}"

    # TEST DATE 
    date = metadata.get("date_begin")
    assert date, f"Date manquante dans doc : {doc}"

    dates.append(date)

# VALIDATION GLOBALE 
assert len(departements) == 1, \
    f"Plusieurs localisations détectées : {departements}"

print("\nTest OK")
print(f"Nombre de documents : {len(docs)}")
print(f"Localisation : {departements}")
print(f"Date min : {min(dates)}")
print(f"Date max : {max(dates)}")


