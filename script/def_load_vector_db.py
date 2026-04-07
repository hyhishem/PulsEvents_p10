import os
from dotenv import load_dotenv

from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS

# charger env
load_dotenv()   


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


