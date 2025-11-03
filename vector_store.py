import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import streamlit as st

class VectorStore:
    def __init__(self):
        self.client = chromadb.Client(Settings(persist_directory="chroma_db"))
        self.collection = self.client.get_or_create_collection("documents")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
                
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        return self.embedding_model.encode(texts).tolist()
            
    def save_document(self, doc_id: str, text: str, embedding: List[float]):
        self.collection.add(documents=[text], embeddings=[embedding], ids=[doc_id])
        
    def get_documents(self) -> Dict:
        return self.collection.get()
        
    def delete_document(self, doc_id: str):
        self.collection.delete(ids=[doc_id])
        st.success(f"Document {doc_id} deleted successfully.")