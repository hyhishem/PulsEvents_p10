import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta,timezone

one_year_ago = (datetime.now(timezone.utc) - timedelta(days=365)).strftime("%Y-%m-%dT00:00:00+00:00")


# Import data à partir de l'API

#Requete via l'api : Essonne - moins d'un an

url_base = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/evenements-publics-openagenda/records/"
params = {
    "lang": "fr",
    "select": "uid,canonicalurl,title_fr,longdescription_fr,firstdate_begin,firstdate_end,location_name,location_address,location_postalcode,location_city,location_department",
    "where": f'firstdate_begin > "{one_year_ago}" AND location_department:"Essonne"',
    "limit": 100,  
    "offset": 0
}

data_complet = []

while True:
    response = requests.get(url_base, params=params)
    if response.status_code != 200:
        print(f"Erreur : {response.status_code}")
        raise SystemExit 

    d= response.json()
    data=d['results']
    
    if not data:
        break

    data_complet.extend(data)
    params["offset"] += params["limit"] 

df = pd.DataFrame.from_dict(data_complet) 


# Prétraitement

df.fillna("", inplace=True)

# Nettoyage texte

def clean_text(text):
    if "<" in text and ">" in text:
        text = BeautifulSoup(text, "html.parser").get_text()
    text = " ".join(text.split())
    text = re.sub(r"[^\w\s.,!?'\-()€:;]", " ", text)
    return text.strip()
       

df["title_fr"] = df["title_fr"].apply(clean_text)
df["longdescription_fr"] = df["longdescription_fr"].apply(clean_text)


df = df[df["title_fr"].notna() & (df["title_fr"].str.strip() != "")]
df = df[df["longdescription_fr"].notna() & (df["longdescription_fr"].str.strip() != "")]

# Conversion dates 
date_cols = [
    "firstdate_begin",
    "firstdate_end"
]

for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors="coerce", utc=True)
    df[col] = df[col].dt.tz_convert("Europe/Paris")
    
df["uid"] = pd.to_numeric(df["uid"],errors="coerce")


df['text_pour_embeding']=df['title_fr']+ '. ' + df['longdescription_fr']


# Sauvegarde en Parquet 


df.to_parquet(
    "data/processed.parquet",
    index=False,
    compression="snappy"   
)
