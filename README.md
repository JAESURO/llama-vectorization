# Smart Document Assistant - README

## 🚀 Overview

Welcome to **Smart Document Assistant**, a powerful web application designed to help you upload, store, and manage documents, as well as ask insightful questions based on the contents of those documents. With the integration of AI models like **Ollama** and tools like **DuckDuckGo Search**, this assistant can help you analyze and retrieve the information you need from both local documents and the web.

### Key Features
- **User Authentication**: Register and log in securely to access personalized features.
- **Document Upload**: Upload and store **PDF** or **TXT** documents.
- **Document Management**: View, delete, and organize documents in your collection.
- **Question Answering**: Ask questions based on the contents of your documents, or search the web for relevant answers.
- **Profanity Filter**: Automatically filters out inappropriate language in documents and queries.
- **Word Cloud Visualization**: Visualize the most frequent terms in your documents with word clouds.

---

## 🧑‍💻 Tech Stack

- **Frontend**: Streamlit (for building interactive UIs)
- **Backend**: Python
- **AI Models**: 
  - **Ollama** for AI-driven responses
  - **SentenceTransformers** for text embedding generation
  - **DuckDuckGo Search API** for web search results
- **Database**: SQLite (for user credentials storage)
- **Document Management**: ChromaDB (for storing and querying document embeddings)
- **Visualization**: Matplotlib and WordCloud (for generating visual representations of text)

---

## 💡 How It Works

### Authentication System
- **Registration**: Users can create an account by choosing a username and password.
- **Login**: Existing users can log in with their credentials.
- **Logout**: Users can log out anytime during the session.

### Document Handling
- **Upload**: Users can upload documents in **PDF** or **TXT** format. The document’s content is cleaned and profaned words are censored before saving.
- **Storage**: Once uploaded, documents are stored in a database with text embeddings generated for future reference.
- **Management**: Users can view a list of saved documents and delete them as needed.

### Question Answering
- **Text Embeddings**: Text from documents is converted into embeddings, which allow for efficient search and retrieval.
- **Ask Questions**: Users can ask questions, and the system will either search for relevant document content or query the web using DuckDuckGo Search.
- **AI-Driven Answers**: Ollama’s language model generates accurate and context-aware answers based on the documents or web search results.

### Visualizations
- **Word Cloud**: Displays a word cloud of the most frequently used words in the document’s text, providing a quick overview of its content.

---

## 📄 How to Run

### Prerequisites
- Python 3.x
- Streamlit (`pip install streamlit`)
- ChromaDB (`pip install chromadb`)
- Sentence-Transformers (`pip install sentence-transformers`)
- PyPDF2 (`pip install PyPDF2`)
- LangChain (`pip install langchain`)
- DuckDuckGoSearch (`pip install duckduckgo-search`)
- Matplotlib (`pip install matplotlib`)
- WordCloud (`pip install wordcloud`)
- Better-Profanity (`pip install better-profanity`)

### Running the Application
1. Clone or download the repository.
2. Install the required dependencies listed above.
3. Run the application with:
   ```
   streamlit run app.py
   ```
4. Access the web app through the provided local address in the terminal.

---

## 🎨 Design

The application features an intuitive and clean user interface:
- **Sidebar**: 
  - Includes options for logging in, logging out, and registering.
  - Displays user status and options for managing documents.
- **Main Area**: 
  - Upload, view, and delete documents.
  - Ask questions and get AI-generated answers.
  - Visualize content through word clouds.

---

## 📜 License

This project is open-source and available under the MIT License. Feel free to use, modify, and distribute the code!

---

### Screenshots

- **User Login Page**:
   ![Login Page](https://github.com/user-attachments/assets/893e2160-54b6-489f-809f-33267f63cc01)
  
- **Document Upload & Management**:
   ![Document Upload](https://github.com/user-attachments/assets/22d8cc89-2f59-4b9c-b59b-8a369dde8fd6)

- **Word Cloud Visualization**:
   ![Word Cloud](https://github.com/user-attachments/assets/36a2212b-0331-4e39-9e84-76164fe445d9)
  
--- 

Enjoy your **Smart Document Assistant** experience! Let AI make your document management smarter! 📚🤖
