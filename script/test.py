from def_load_vector_db import load_vector_db

from dotenv import load_dotenv
import os


vector_db = load_vector_db()

# récupération de tous les documents

docs = list(vector_db.docstore._dict.values())
assert len(docs) > 0, "La base est vide"


departements = set()
dates = []

for doc in docs:
    metadata = doc.metadata

    # Test localisation
    location_department = metadata.get("location_department", "").lower()
    assert location_department, f"Ville manquante dans doc : {doc}"

    departements.add(location_department)
    assert "essonne" in location_department, f"Ville hors Essonne : {location_department}"

    # Test date_begin existe et stockage dans dates
    date = metadata.get("date_begin")
    assert date, f"Date manquante dans doc : {doc}"

    dates.append(date)

# VALIDATION 
assert len(departements) == 1, f"Plusieurs localisations détectées : {departements}"

print(50*'-')
print("Test OK")
print(50*'-')
print(f"Nombre de documents : {len(docs)}")
print(f"Localisation : {departements}")
print(f"Date min : {min(dates)}")
print(f"Date max : {max(dates)}")


