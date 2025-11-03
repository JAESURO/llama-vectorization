# Smart Document Assistant - README

## 🚀 Overview

Welcome to **Smart Document Assistant**, a powerful web application designed to help you upload, store, and manage documents, as well as ask insightful questions based on the contents of those documents. With the integration of **Ollama** AI models, this assistant helps you analyze and retrieve information from your local documents.

### Key Features
- **User Authentication**: Register and log in securely to access personalized features.
- **Document Upload**: Upload and store **PDF** or **TXT** documents.
- **Document Management**: View, delete, and organize documents in your collection.
- **Question Answering**: Ask questions based on the contents of your documents using AI.
- **Profanity Filter**: Automatically filters out inappropriate language in documents and queries.
- **Word Cloud Visualization**: Visualize the most frequent terms in your documents with word clouds.

---

## 🧑‍💻 Tech Stack

- **Frontend**: Streamlit (for building interactive UIs)
- **Backend**: Python
- **AI Models**: 
  - **Ollama** for AI-driven responses (Llama 3.2 3B model)
  - **SentenceTransformers** for text embedding generation
- **Database**: SQLite (for user credentials storage)
- **Vector Storage**: ChromaDB (for storing and querying document embeddings)
- **Visualization**: Matplotlib and WordCloud (for generating visual representations of text)

---

## 💡 How It Works

### Authentication System
- **Registration**: Users can create an account by choosing a username and password.
- **Login**: Existing users can log in with their credentials.
- **Logout**: Users can log out anytime during the session.

### Document Handling
- **Upload**: Users can upload documents in **PDF** or **TXT** format. The document's content is cleaned and profaned words are censored before saving.
- **Storage**: Once uploaded, documents are stored in ChromaDB with text embeddings generated for future reference.
- **Management**: Users can view a list of saved documents and delete them as needed.

### Question Answering
- **Text Embeddings**: Text from documents is converted into embeddings, which allow for efficient search and retrieval.
- **Ask Questions**: Users can ask questions, and the system searches for relevant content from uploaded documents.
- **AI-Driven Answers**: Ollama's Llama 3.2 3B model generates accurate and context-aware answers based on the document content.

### Visualizations
- **Word Cloud**: Displays a word cloud of the most frequently used words in the document's text, providing a quick overview of its content.

---

## 📁 Project Structure

```
llama-vectorization/
├── app.py                  # Main Streamlit application
├── document_assistant.py   # Main coordinator class
├── database.py            # User authentication and SQLite operations
├── vector_store.py        # ChromaDB operations and embeddings
├── ai_assistant.py        # Ollama integration and AI responses
├── document_processor.py  # Text extraction and profanity filtering
├── visualizer.py         # Word cloud generation
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

---

## 📄 How to Run

### Prerequisites
- Python 3.x
- Ollama installed and running (see [Ollama Installation](https://ollama.com))

### Installation

1. Clone or download the repository.

2. Install Ollama:
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

3. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Pull the Llama 3.2 3B model (if not already installed):
   ```bash
   ollama pull llama3.2:3b
   ```

### Running the Application

1. Make sure Ollama is running:
   ```bash
   ollama serve
   ```

2. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

3. Access the web app through the provided local address in the terminal (usually `http://localhost:8501`).

---

## 🎨 Design

The application features an intuitive and clean user interface:
- **Sidebar**: 
  - Includes options for logging in, logging out, and registering.
  - Displays user status and current AI model information.
- **Main Area**: 
  - Upload, view, and delete documents.
  - Ask questions and get AI-generated answers based on document content.
  - Visualize content through word clouds.
  - View chat history.

---

## 📜 License

This project is open-source and available under the MIT License. Feel free to use, modify, and distribute the code!

---

Enjoy your **Smart Document Assistant** experience! Let AI make your document management smarter! 📚🤖
