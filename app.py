import streamlit as st
from llama_index.core.llms import ChatMessage
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

# Function to search the web using DuckDuckGo
def web_search(query, max_results=10):
    search_results = DDGS().text(query, max_results=max_results)
    return "\n".join([result["body"] for result in search_results if "body" in result])

# Function to generate and display WordCloud
def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

# LangChain setup
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
    You are an intelligent chatbot. Answer the question based on the context provided.
    Context: {context}
    Question: {question}
    """
)
llm_chain = LLMChain(llm=LangOllama(model="llama3.2"), prompt=prompt_template)

# Streamlit UI
st.header("Add a New Document")
uploaded_file = st.file_uploader("Choose a PDF or TXT file", type=["pdf", "txt"])

if uploaded_file is not None:
    document_text = extract_text_from_pdf(uploaded_file) if uploaded_file.type == "application/pdf" else uploaded_file.getvalue().decode("utf-8")
    st.text_area("Document Content", document_text, height=300)
    with st.form("add_document_form"):
        submit_button = st.form_submit_button("Add Document")
        if submit_button and document_text:
            doc_embedding = generate_embeddings([document_text])[0]
            doc_id = f"doc_{len(get_stored_documents()["documents"]) + 1}"
            save_document(doc_id, document_text, doc_embedding)
            st.success(f"Document added successfully with ID: {doc_id}")
            generate_wordcloud(document_text)

st.sidebar.header("Model Configuration")
selected_model = st.sidebar.selectbox("Select a model:", ["llama3.2"])

st.header("Ask a Question")
user_question = st.text_input("Enter your question:")

if user_question:
    query_embedding = generate_embeddings([user_question])[0]
    relevant_results = query_relevant_documents(query_embedding)
    context = " ".join(doc if isinstance(doc, str) else " ".join(doc) for doc in relevant_results["documents"]) if relevant_results.get("documents", []) else ""
    
    if not context:
        context = web_search(user_question)
    
    chat_response = llm_chain.run({"context": context, "question": user_question})
    st.write(f"### Assistant's Response:\n{chat_response}")
    generate_wordcloud(chat_response)

st.header("View Stored Documents")
stored_documents = get_stored_documents()
if stored_documents and "documents" in stored_documents:
    for i, doc in enumerate(stored_documents["documents"], start=1):
        with st.expander(f"Document {i}"):
            st.write(doc)
            generate_wordcloud(doc)