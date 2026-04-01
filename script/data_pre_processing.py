import requests
import pandas as pd
import re


# =========================
# Import data à partir de l'API
# =========================


#Requete via l'api : Essonne à partir du 20 Mars 2025

url_base = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/evenements-publics-openagenda/records/"
params = {
    "lang": "fr",
    "select": "uid,title_fr,longdescription_fr,daterange_fr,firstdate_begin,firstdate_end,lastdate_begin,lastdate_end,location_name,location_address,location_postalcode,location_city",
    "where": 'firstdate_begin > "2025-03-20T00:00:00+00:00" AND location_department:"Essonne"',
    "limit": 100,  
    "offset": 0
}

data_complet = []

while True:
    response = requests.get(url_base, params=params)
    # verifier si 200 => OK
    if response.status_code != 200:
        print(f"Erreur : {response.status_code}")
        raise SystemExit 

    d= response.json()
    data=d['results']
    
    if not data:
        break

    data_complet.extend(data)
    params["offset"] += params["limit"] 

df = pd.DataFrame.from_dict(data_complet) # convertir  en df les results 


# =========================
# Préprocess
# =========================


df.fillna("", inplace=True)

# Nettoyage texte
def clean_text(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text)       
    text = re.sub(r'[^\w\s.,!?\'"-()]', ' ', text)
    return text.strip()

df["title_fr"] = df["title_fr"].apply(clean_text)
df["longdescription_fr"] = df["longdescription_fr"].apply(clean_text)
#df["keywords_clean"] = df["keywords_fr"].apply(clean_text)

# Conversion des dates en datetime
date_cols = [
    "firstdate_begin",
    "firstdate_end",
    "lastdate_begin",
    "lastdate_end"
]

for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors="coerce", utc=True)
    df[col] = df[col].dt.tz_convert("Europe/Paris")
    
df["uid"] = pd.to_numeric(df["uid"], errors="coerce")

# =========================
# Resumé
# =========================

print("Shape final :", df.shape)
print(df.dtypes)

df['text_embeding']=df['title_fr']+ '. ' + df['longdescription_fr']


