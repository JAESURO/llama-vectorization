import streamlit as st
import logging
import chromadb
from chromadb.config import Settings
from llama_index.llms.ollama import Ollama
from sentence_transformers import SentenceTransformer
import PyPDF2
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import Ollama as LangOllama
import duckduckgo_search as ddg
from duckduckgo_search import DDGS
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from better_profanity import profanity
import sqlite3

logging.basicConfig(level=logging.INFO)

st.set_page_config(page_title="Smart Document Assistant", page_icon="📄", layout="wide")

client = chromadb.Client(Settings(persist_directory="chromadb_data"))
collection = client.get_or_create_collection("documents")

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY, 
    password TEXT
)''')
conn.commit()

def register():
    st.sidebar.header("📝 Register New User")
    new_username = st.sidebar.text_input("Choose a Username")
    new_password = st.sidebar.text_input("Choose a Password", type="password")
    if st.sidebar.button("Register"):
        cursor.execute("SELECT * FROM users WHERE username=?", (new_username,))
        if cursor.fetchone():
            st.sidebar.error("🚫 Username already exists!")
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_username, new_password))
            conn.commit()
            st.sidebar.success("✅ Registration successful! You can now log in.")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""

def login():
    st.sidebar.header("🔐 User Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        if cursor.fetchone():
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.sidebar.success(f"Welcome {username}!")
        else:
            st.sidebar.error("Invalid credentials!")

register()

if not st.session_state["logged_in"]:
    login()
else:
    st.sidebar.write(f"Logged in as {st.session_state['username']}")
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.sidebar.warning("Logged out!")

def check_profanity(text):
    return profanity.contains_profanity(text)

def clean_text(text):
    return profanity.censor(text)

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

def save_document(doc_id, text, embedding):
    collection.add(documents=[text], embeddings=[embedding], ids=[doc_id])

def get_stored_documents():
    return collection.get()

def generate_embeddings(texts):
    return embedding_model.encode(texts)

st.header("📂 Upload a New Document")
if st.session_state["logged_in"]:
    uploaded_file = st.file_uploader("Choose a PDF or TXT file", type=["pdf", "txt"])
    if uploaded_file:
        document_text = uploaded_file.getvalue().decode("utf-8") if uploaded_file.type == "text/plain" else ""
        document_text = clean_text(document_text)
        st.text_area("📖 Document Preview", document_text[:2000] + "..." if len(document_text) > 2000 else document_text, height=200)
        if st.button("🚀 Add Document"):
            doc_embedding = generate_embeddings([document_text])[0]
            doc_id = f"doc_{len(get_stored_documents()['documents']) + 1}"
            save_document(doc_id, document_text, doc_embedding)
            st.success(f"✅ Document added successfully with ID: {doc_id}")
else:
    st.warning("Please log in to upload documents.")

st.header("💡 Ask a Question")
user_question = st.text_input("✏ Enter your question:")
if user_question:
    if check_profanity(user_question):
        st.warning("⚠️ Your query contains inappropriate words.")
    else:
        st.session_state["chat_history"].append({"user": user_question})
        query_embedding = generate_embeddings([user_question])[0]
        relevant_results = get_stored_documents()
        context = " ".join(relevant_results["documents"]) if relevant_results.get("documents") else "No relevant documents found."
        st.session_state["chat_history"].append({"bot": context})
        st.write(f"### 🤖 Assistant's Response:\n{context}")

st.header("📜 Chat History")
for chat in st.session_state["chat_history"]:
    if "user" in chat:
        st.write(f"**User:** {chat['user']}")
    if "bot" in chat:
        st.write(f"**Bot:** {chat['bot']}")