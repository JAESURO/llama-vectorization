from database import DatabaseManager
from vector_store import VectorStore
from ai_assistant import AIAssistant
from document_processor import DocumentProcessor
from visualizer import Visualizer
import streamlit as st

class DocumentAssistant:
    def __init__(self):
        self.db = DatabaseManager()
        self.vector_store = VectorStore()
        self.ai = AIAssistant()
        self.processor = DocumentProcessor()
        self.visualizer = Visualizer()
        
    def fetch_relevant_context(self, question: str) -> str:
        relevant_results = self.vector_store.get_documents()
        
        if relevant_results.get("documents"):
            return " ".join(relevant_results["documents"])
        else:
            return "No relevant documents found."