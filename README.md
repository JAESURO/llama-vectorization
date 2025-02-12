Streamlit Document Management & Q&A Application

This project is a Streamlit-based web application that allows users to upload and store documents, generate embeddings, perform semantic searches, and ask questions based on stored documents or web searches.

Features

Document Upload: Supports PDF and TXT file uploads.

Embedding Storage: Generates and stores embeddings using SentenceTransformer.

ChromaDB Integration: Stores and retrieves document embeddings for semantic search.

Q&A System: Uses LangChain and Ollama models to generate answers based on document context or web search.

Web Search: Fetches relevant information using DuckDuckGo if no relevant document is found.

Streamlit UI: Provides a simple and interactive interface.

Dependencies

To run this project, install the following dependencies:

pip install streamlit llama-index chromadb sentence-transformers PyPDF2 langchain duckduckgo-search

Setup Instructions

Clone the repository:

git clone <repository-url>
cd <project-folder>

Install dependencies:

pip install -r requirements.txt

Run the Streamlit application:

streamlit run app.py

File Structure

project-folder/
│── app.py               # Main Streamlit application
│── requirements.txt     # Required Python dependencies
│── README.md            # Documentation (this file)
│── chromadb_data/       # Persistent storage for ChromaDB

Usage

Upload a document:

Select a PDF or TXT file to upload.

View the extracted content in the text area.

Click "Add Document" to store it.

Ask a question:

Enter a question in the text input field.

The app searches relevant documents in ChromaDB.

If no documents are found, it searches the web using DuckDuckGo.

The AI model generates a response based on the retrieved information.

Configuration

The model used for responses is configured in the sidebar.

ChromaDB stores documents persistently in the chromadb_data/ directory.

Future Enhancements

Support for additional file formats.

User authentication and document access control.

Improved response generation using fine-tuned models.

License

This project is licensed under the MIT License.

