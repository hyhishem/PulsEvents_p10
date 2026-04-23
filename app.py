from script.def_load_vector_db import load_vector_db
import streamlit as st

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough,RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from datetime import datetime, timedelta,timezone
from dotenv import load_dotenv
import os

today = datetime.now(timezone.utc).strftime("%Y-%m-%d")


# config
load_dotenv() 


# LLM 
llm = ChatMistralAI(
    model=os.getenv("LLM_MODEL"),
    api_key=os.getenv("MISTRAL_API_KEY"),
)

# load vector db
@st.cache_resource
def get_db():
    return load_vector_db()


try:
    vector_db = get_db()
    st.success("Base de connaissances chargée avec succès")
except Exception as e:
    st.error(f"Erreur lors du chargement de la base : {e}")
    st.stop()


# prompt 
prompt_template = ChatPromptTemplate.from_template("""
Tu es un assistant spécialisé dans les événements culturels dans l'Essonne.
Utilise uniquement le contexte pour répondre.

Contexte :
{context}

Question :
{question}

Réponse :

Si tu ne sais pas, dis-le clairement.
Utilise la date d'aujourd'hui  qui est {date} pour répondre 

""")


# pipelin RAG

rag_chain = (
    {"context":vector_db.as_retriever(search_kwargs={"k": 15}) , "question": RunnablePassthrough()}
    | RunnableLambda(lambda x: {**x, "date": today})
    | prompt_template
    | llm
    | StrOutputParser()
)

# Streamlit 

st.title("Puls-Events: Assistant d'événements culturels")
st.markdown("Posez vos questions sur les événements culturels dans Essonne")


# Zone de saisie et reponse
if prompt := st.chat_input("Exemple : Indique-moi un événement pour les étudiants?"):
    
    # Affichage du message utilisateur
    with st.chat_message("user"):
        st.markdown(prompt)

    # Affichage du message assistant
    with st.chat_message("assistant"):
        with st.spinner("Recherche des événements..."):
            response = rag_chain.invoke(prompt)     
        st.markdown(response)



