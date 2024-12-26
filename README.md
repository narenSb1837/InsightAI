# 🚀 *Overview*  
This project is a chatbot designed to process and answer questions from uploaded PDF documents with minimal hallucinations. By leveraging *semantic chunking, **vector embeddings, and **LLM-based citation engines*, the chatbot ensures accurate responses with reliable citations.

---

## 🛠️ *Tech Stack*  

•⁠  ⁠*Programming Language:* Python  
•⁠  ⁠*Vector Database:* Pinecone  
•⁠  ⁠*LLM:* LLaMA-3  
•⁠  ⁠*Similarity Metric:* Cosine Similarity (Threshold: *80%*)  

---

## 📑 *Workflow*

### *1. PDF Upload and Preprocessing*  
•⁠  ⁠The uploaded PDF is split into *semantic chunks* to maintain contextual integrity.  
•⁠  ⁠Chunks are optimized to balance size and semantic meaning.

### *2. Embedding and Storage*  
•⁠  ⁠Each chunk is converted into *embedding vectors* using the embedding model.  
•⁠  ⁠These embeddings are stored in *Pinecone* for efficient similarity searches.  

### *3. User Query*  
•⁠  ⁠The user submits a query to the chatbot.  
•⁠  ⁠The query is converted into an *embedding vector* using the same embedding model.  

### *4. Similarity Search*  
•⁠  ⁠A *cosine similarity* search is performed in Pinecone.  
•⁠  ⁠The *top 5 most similar chunks* (with a similarity score ≥ 80%) are retrieved and ranked in descending order of relevance.  

### *5. Query Processing with LLaMA-3*  
•⁠  ⁠The top 5 chunks are passed to *LLaMA-3* for query resolution.  
•⁠  ⁠LLaMA-3 uses a *citation query engine* and a *reranking model* to:  
   - Provide a precise *answer*.  
   - Include *source citations* to ensure trustworthiness and reduce hallucinations.  

---

## 📊 *Key Features*  
•⁠  ⁠✅ *Accurate Information Retrieval:* Semantic chunking ensures context-aware search results.  
•⁠  ⁠✅ *Minimal Hallucinations:* Citation-based answers improve reliability.  
•⁠  ⁠✅ *Efficient Search with Pinecone:* Real-time querying with vector embeddings.  
•⁠  ⁠✅ *Scalable Design:* Supports large documents without performance degradation.  

---

## 🧠 *How It Works (High-Level Architecture)*  

1.⁠ ⁠*PDF ➡️ Chunking ➡️ Embedding ➡️ Pinecone Storage*  
2.⁠ ⁠*User Query ➡️ Embedding ➡️ Similarity Search (Top 5 Chunks)*  
3.⁠ ⁠*Top 5 Chunks ➡️ LLaMA-3 Processing ➡️ Reranking & Citation Engine*  
4.⁠ ⁠*Response with Citations*  

