from fastapi import FastAPI, File, UploadFile, HTTPException
from models import QueryInput, QueryResponse, DocumentInfo, DeleteFileRequest
from db_utils import get_chat_history, get_pinecone_index, index_document_to_pinecone
from llama_index.llms.groq import Groq
from config import Config
import os
import uuid
import logging
import shutil
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.core.query_engine import CitationQueryEngine

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# Initialize FastAPI app
app = FastAPI()

@app.post("/chat", response_model=QueryResponse)
def chat(query_input: QueryInput):
    logging.info(f", User Query: {query_input.question} ")
    Settings.embed_model = FastEmbedEmbedding(model_name="BAAI/bge-small-en-v1.5")
    Settings.llm = Groq(model="llama3-8b-8192", api_key=Config.GROQ_API_KEY)
    vector_store = PineconeVectorStore(pinecone_index=get_pinecone_index())
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    
    query_engine = CitationQueryEngine.from_args(index,similarity_top_k=3,citation_chunk_size=512)
    
    answer = query_engine.query(query_input.question)
    logging.info(f" AI Response: {answer}")
    
    return QueryResponse(answer=str(answer))

@app.post("/upload-doc")
def upload_and_index_document(file: UploadFile = File(...)):
    print("\n \n file",file)
    allowed_extensions = ['.pdf', '.docx', '.html','.txt']
    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Unsupported file type. Allowed types are: {', '.join(allowed_extensions)}")
    file_name = os.path.basename(file.filename)
    temp_file_path = f"uploaded_files/{file_name}"

    try:
        # Save the uploaded file to a temporary file
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        
        success = index_document_to_pinecone(temp_file_path)

        if success:
            return {"message": f"File {file.filename} has been successfully uploaded and indexed."}
        else:
            raise HTTPException(status_code=500, detail=f"Failed to index {file.filename}.")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


