from def_load_vector_db import load_vector_db
from datetime import datetime, timedelta,timezone
from dotenv import load_dotenv
import os

def test():

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

    # Test date_begin la plus ancienne moins d'un an 
    one_year_ago = (datetime.now(timezone.utc) - timedelta(days=365)).strftime("%Y-%m-%dT00:00:00+00:00")
    assert min(dates)>=one_year_ago , f"Attention le plus anciens événement commence le {min(dates)} "


    # VALIDATION 
    assert len(departements) == 1, f"Plusieurs localisations détectées : {departements}"






