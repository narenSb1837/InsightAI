import os
from dotenv import load_dotenv

env_file = ".env"
load_dotenv(env_file)


class Config():
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    COHERE_API_KEY = os.environ.get("COHERE_API_KEY")
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI")
    MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME")
    PINECONE_API =  os.environ.get("PINECONE_API_KEY")