import pymongo
from pymongo import MongoClient
import os
from datetime import datetime
from config import Config
import pytz  
from constant import Collections
from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.core import Settings
from llama_index.core.node_parser import SemanticSplitterNodeParser
from pinecone import Pinecone, ServerlessSpec
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

def get_db_connection():
    client = MongoClient(Config.MONGO_DB_URI)
    return client

def get_pinecone_index():
    pc = Pinecone(api_key=Config.PINECONE_API)
    pinecone_index = pc.Index("test")   
    return pinecone_index

def store_chat_interaction(query, response):
    # Get the client
    client = get_db_connection()
    db = client[Config.MONGO_DB_NAME]
    cht_history = db[Collections.CHAT_HISTORY]

    current_datetime = datetime.now()
    ist_timezone = pytz.timezone('Asia/Kolkata')
    current_time_ist = current_datetime.astimezone(ist_timezone)
    current_datetime = current_time_ist.strftime("%Y-%m-%d %H:%M:%S")

    cht_history.insert_one({
        'query': query,
        'response': response,
        'time': current_datetime
    })

    # Close the client connection
    client.close()
    
def index_document_to_pinecone(file_path):
    try:
        documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
        Settings.embed_model = FastEmbedEmbedding(model_name="BAAI/bge-small-en-v1.5")
        pinecone_index = get_pinecone_index()
        vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

        return True

    except Exception as e:
        return False

def get_chat_history():
    """ returns the recent 5 conversations """
    ist_timezone=pytz.timezone('Asia/Kolkata')
    cursor=cht_info.find().sort('time',pymongo.DESCENDING).limit(5)
    latest_cht_history=list()
    for doc in cursor:
        qury=doc['query']
        resp=doc['response']
        tim=doc['time']
        latest_cht_history.append((qury,resp))
    return latest_cht_history