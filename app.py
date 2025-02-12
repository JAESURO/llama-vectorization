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
from langchain.tools import DuckDuckGoSearchResults  # Import DuckDuckGoSearchResults
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import sqlite3
from better_profanity import profanity

# Configure logging
logging.basicConfig(level=logging.INFO)

# Streamlit page settings
st.set_page_config(page_title="Smart Document Assistant", page_icon="📄", layout="wide")

# Initialize database connection
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
conn.commit()

# Initialize ChromaDB client
client = chromadb.Client(Settings(persist_directory="chromadb_data"))
collection = client.get_or_create_collection("documents")

# Load embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize DuckDuckGo Search
ddg_search = DuckDuckGoSearchResults()  # Initialize DuckDuckGo search tool

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# ---------- Authentication System ----------
def register():
    """Handles user registration."""
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

def login():
    """Handles user login."""
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

def logout():
    """Logs out the current user."""
    st.session_state["logged_in"] = False
    st.sidebar.warning("Logged out!")

register()

if not st.session_state["logged_in"]:
    login()
else:
    st.sidebar.write(f"Logged in as {st.session_state['username']}")
    if st.sidebar.button("Logout"):
        logout()

# ---------- Document Handling ----------
def check_profanity(text):
    """Checks if the text contains profanity."""
    return profanity.contains_profanity(text)

def clean_text(text):
    """Cleans text by censoring profanity."""
    return profanity.censor(text)

def save_document(doc_id, text, embedding):
    """Saves document embeddings in ChromaDB."""
    collection.add(documents=[text], embeddings=[embedding], ids=[doc_id])

def get_stored_documents():
    """Retrieves stored documents from ChromaDB."""
    return collection.get()

def delete_document(doc_id):
    """Deletes a document from ChromaDB."""
    collection.delete(ids=[doc_id])
    st.success(f"✅ Document {doc_id} deleted successfully.")

def generate_embeddings(texts):
    """Generates embeddings for given text."""
    return embedding_model.encode(texts)

# ---------- File Upload ----------
def handle_file_upload():
    """Handles PDF or TXT file upload and embedding storage."""
    st.header("📂 Upload a New Document")

    uploaded_file = st.file_uploader("Choose a PDF or TXT file", type=["pdf", "txt"])
    if uploaded_file:
        if uploaded_file.type == "text/plain":
            document_text = uploaded_file.getvalue().decode("utf-8")
        else:
            reader = PyPDF2.PdfReader(uploaded_file)  # Fix: No 'with' statement
            document_text = " ".join([page.extract_text() or "" for page in reader.pages])  # Handle None case

        document_text = clean_text(document_text)
        st.text_area("📖 Document Preview", document_text[:2000] + "..." if len(document_text) > 2000 else document_text, height=200)

        if st.button("🚀 Add Document"):
            doc_embedding = generate_embeddings([document_text])[0]
            doc_id = f"doc_{len(get_stored_documents().get('documents', [])) + 1}"
            save_document(doc_id, document_text, doc_embedding)
            st.success(f"✅ Document added successfully with ID: {doc_id}")

# ---------- View and Delete Documents ----------
def view_and_delete_documents():
    """Displays all saved documents and allows deletion."""
    st.header("📚 Saved Documents")
    documents = get_stored_documents()

    if documents.get("documents"):
        for doc_id, doc_text in zip(documents["ids"], documents["documents"]):
            with st.expander(f"📄 Document ID: {doc_id}"):
                st.write(doc_text[:1000] + "..." if len(doc_text) > 1000 else doc_text)
                if st.button(f"❌ Delete {doc_id}"):
                    delete_document(doc_id)
                    st.rerun()  # Refresh the page to reflect changes
    else:
        st.write("No documents found.")

# ---------- Question Answering ----------
def fetch_relevant_context(question):
    """Fetches relevant documents from ChromaDB or searches the web."""
    query_embedding = generate_embeddings([question])[0]
    relevant_results = get_stored_documents()

    if relevant_results.get("documents"):
        return " ".join(relevant_results["documents"])
    else:
        st.write("📡 No relevant documents found. Searching the web...")
        search_results = ddg_search.run(question)  # Use DuckDuckGoSearchResults
        return search_results if search_results else "No relevant results."

def generate_response(question, context):
    """Generates an AI response using the Ollama model."""
    ollama_llm = LangOllama(model="llama3.2")

    prompt_template = """You are an AI assistant that answers questions based on the following context:
    {context}

    Question: {question}
    Answer:"""

    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = LLMChain(llm=ollama_llm, prompt=prompt)

    return chain.run({"context": context, "question": question})

def handle_question_answering():
    """Handles user input and AI response generation."""
    st.header("💡 Ask a Question")
    user_question = st.text_input("✏ Enter your question:")

    if user_question:
        if check_profanity(user_question):
            st.warning("⚠️ Your query contains inappropriate words.")
            return

        st.session_state["chat_history"].append({"user": user_question})
        context = fetch_relevant_context(user_question)
        response = generate_response(user_question, context)

        st.session_state["chat_history"].append({"bot": response})
        st.write(f"### 🤖 Assistant's Response:\n{response}")

        visualize_text_analysis(context)

# ---------- Visualization ----------
def visualize_text_analysis(text):
    """Generates and displays word cloud."""
    if text:
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)

# ---------- Chat History ----------
def display_chat_history():
    """Displays the chat history."""
    st.header("📜 Chat History")
    for chat in st.session_state["chat_history"]:
        if "user" in chat:
            st.write(f"**User:** {chat['user']}")
        if "bot" in chat:
            st.write(f"**Bot:** {chat['bot']}")

# ---------- Main Execution ----------
if st.session_state["logged_in"]:
    handle_file_upload()
    view_and_delete_documents()  # Add this function to view and delete documents
    handle_question_answering()
    display_chat_history()
else:
    st.warning("Please log in to upload documents and ask questions.")