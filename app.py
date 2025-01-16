import streamlit as st
from llama_index.core.llms import ChatMessage
import logging
import chromadb
from chromadb.config import Settings
from llama_index.llms.ollama import Ollama
from sentence_transformers import SentenceTransformer
import PyPDF2

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize ChromaDB client and collection
client = chromadb.Client(Settings(persist_directory="chromadb_data"))
collection = client.get_or_create_collection("documents")

# Load SentenceTransformer model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to generate embeddings
def generate_embeddings(texts):
    return embedding_model.encode(texts)

# Function to save a document and its embedding to ChromaDB
def save_document(doc_id, text, embedding):
    collection.add(documents=[text], embeddings=[embedding], ids=[doc_id])

# Function to retrieve all stored documents
def get_stored_documents():
    return collection.get()

# Function to query relevant documents
def query_relevant_documents(query_embedding, top_k=1):
    try:
        results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
        return results
    except Exception as e:
        logging.error(f"Error querying ChromaDB: {str(e)}")
        return {"documents": []}

# Function to generate a response based on the context and user query
def generate_response(model_name, messages):
    if not model_name:
        raise ValueError("Model name is required.")
    
    llm = Ollama(model=model_name, request_timeout=120.0)
    response = ""
    for message_chunk in llm.stream_chat(messages):
        response += message_chunk.delta
    return response

# Function to extract text from PDF file
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Section: Add Document
st.header("Add a New Document")

# File uploader for PDF and TXT files
uploaded_file = st.file_uploader("Choose a PDF or TXT file", type=["pdf", "txt"])

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        # Extract text from PDF
        document_text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "text/plain":
        # Read text from TXT file
        document_text = uploaded_file.getvalue().decode("utf-8")

    # Show the extracted content for user verification
    st.text_area("Document Content", document_text, height=300)

    with st.form("add_document_form"):
        submit_button = st.form_submit_button("Add Document")
        if submit_button and document_text:
            doc_embedding = generate_embeddings([document_text])[0]
            doc_id = f"doc_{len(get_stored_documents()['documents']) + 1}"
            save_document(doc_id, document_text, doc_embedding)
            st.success(f"Document added successfully with ID: {doc_id}")

# Sidebar: Model Selection
st.sidebar.header("Model Configuration")
selected_model = st.sidebar.selectbox(
    "Select a model for response generation:",
    ["llama3.2"]
)

# Section: Query and Chat
st.header("Ask a Question")
user_question = st.text_input("Enter your question:")

if user_question:
    # Generate embedding for the query
    query_embedding = generate_embeddings([user_question])[0]

    # Retrieve relevant documents
    relevant_results = query_relevant_documents(query_embedding)

    if relevant_results.get("documents", []):
        # Combine retrieved documents into context
        context = " ".join(doc if isinstance(doc, str) else " ".join(doc) for doc in relevant_results["documents"])
        
        # Update chat history
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        st.session_state.chat_history.append({"role": "user", "content": user_question})

        # Add context explicitly for the assistant to use
        chat_messages = [
            ChatMessage(role="system", content=f"Use the following context for your response: {context}"),
            *[ 
                ChatMessage(role=msg["role"], content=msg["content"]) 
                for msg in st.session_state.chat_history
            ]
        ]

        # Generate response using the model
        try:
            assistant_response = generate_response(selected_model, chat_messages)
            st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
            st.write(f"### Assistant's Response:\n{assistant_response}")
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
    else:
        st.write("No relevant documents found for your query.")
