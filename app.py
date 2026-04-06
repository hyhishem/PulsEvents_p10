import streamlit as st
from dotenv import load_dotenv
import os

from langchain_mistralai import MistralAIEmbeddings, ChatMistralAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# config
load_dotenv() #charge les variables env


# CONFIGURATION DU LLM 
llm = ChatMistralAI(
    model=os.getenv("LLM_MODEL"),
    api_key=os.getenv("MISTRAL_API_KEY"),
)

# CHARGEMENT DE LA BASE VECTORIELLE 
@st.cache_resource
def load_vector_db():
    embeddings = MistralAIEmbeddings(
        model=os.getenv("EMBEDDING_MODEL"),
        api_key=os.getenv("MISTRAL_API_KEY")
    )
    return FAISS.load_local(
        folder_path=os.getenv("VECTOR_DB_PATH"),
        embeddings=embeddings,
        allow_dangerous_deserialization=True
    )


try:
    vector_db = load_vector_db()
    st.success("Base de connaissances chargée avec succès")
except Exception as e:
    st.error(f"Erreur lors du chargement de la base : {e}")
    st.stop()


# PROMPT 
prompt_template = ChatPromptTemplate.from_template("""
Tu es un assistant spécialisé dans les événements culturels dans l'Essonne.
Utilise uniquement le contexte pour répondre.
Si tu ne sais pas, dis-le clairement.

Contexte :
{context}

Question :
{question}

Réponse :
""")


# pipelin RAG

rag_chain = (
    {"context": vector_db.as_retriever() , "question": RunnablePassthrough()}
    | prompt_template
    | llm
    | StrOutputParser()
)

# STREAMLIT 

st.title("Puls-Events - Assistant Événements Culturels")
st.markdown("Posez vos questions sur les événements culturels dans Essonne")


# Zone de saisie
if prompt := st.chat_input("Exemple : Je souhaite assister à un concert à partir d'avril 2026 ?"):
    
    # Affichage du message utilisateur
    with st.chat_message("user"):
        st.markdown(prompt)

    # Affichage du message assistant
    with st.chat_message("assistant"):
        with st.spinner("Recherche des événements..."):
            response = rag_chain.invoke(prompt)     
        st.markdown(response)



