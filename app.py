import streamlit as st
from document_assistant import DocumentAssistant

st.set_page_config(page_title="Smart Document Assistant", page_icon="📄", layout="wide")

@st.cache_resource
def get_assistant():
    return DocumentAssistant()

assistant = get_assistant()

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

def register():
    st.sidebar.header("📝 Register New User")
    new_username = st.sidebar.text_input("Choose a Username")
    new_password = st.sidebar.text_input("Choose a Password", type="password")

    if st.sidebar.button("Register"):
        if assistant.db.register_user(new_username, new_password):
            st.sidebar.success("✅ Registration successful! You can now log in.")
        else:
            st.sidebar.error("🚫 Username already exists!")

def login():
    st.sidebar.header("🔐 User Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if assistant.db.authenticate_user(username, password):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.sidebar.success(f"Welcome {username}!")
        else:
            st.sidebar.error("Invalid credentials!")

def logout():
    st.session_state["logged_in"] = False

def handle_file_upload():
    st.header("📂 Upload a New Document")
    uploaded_file = st.file_uploader("Choose a PDF or TXT file", type=["pdf", "txt"])
    
    if uploaded_file:
        document_text = assistant.processor.extract_text_from_file(uploaded_file)
        document_text = assistant.processor.clean_text(document_text)
        st.text_area("📖 Document Preview", 
                    document_text[:2000] + "..." if len(document_text) > 2000 else document_text, 
                    height=200)

        if st.button("🚀 Add Document"):
            doc_embedding = assistant.vector_store.generate_embeddings([document_text])[0]
            doc_id = f"doc_{len(assistant.vector_store.get_documents().get('documents', [])) + 1}"
            assistant.vector_store.save_document(doc_id, document_text, doc_embedding)
            st.success(f"✅ Document added successfully with ID: {doc_id}")

def view_and_delete_documents():
    st.header("📚 Saved Documents")
    documents = assistant.vector_store.get_documents()

    if documents.get("documents"):
        for doc_id, doc_text in zip(documents["ids"], documents["documents"]):
            with st.expander(f"📄 Document ID: {doc_id}"):
                st.write(doc_text[:1000] + "..." if len(doc_text) > 1000 else doc_text)
                if st.button(f"❌ Delete {doc_id}"):
                    assistant.vector_store.delete_document(doc_id)
                    st.rerun()
    else:
        st.write("No documents found.")

def handle_question_answering():
    st.header("💡 Ask a Question")
    
    model_name = assistant.ai.current_model if assistant.ai.current_model else "Unknown"
    st.info(f"🤖 Using AI Model: {model_name}")
    
    if "llama3.2:3b" not in model_name.lower():
        if st.button("📥 Pull Llama 3.2 3B"):
            with st.spinner("Downloading Llama 3.2 3B... This may take several minutes."):
                if assistant.ai.pull_llama3_2_3b():
                    st.success("✅ Llama 3.2 3B downloaded successfully! Please restart the app.")
                    st.rerun()
                else:
                    st.error("❌ Failed to download Llama 3.2 3B. Please check Ollama installation.")
    
    user_question = st.text_input("✏ Enter your question:")

    if user_question:
        if assistant.processor.check_profanity(user_question):
            return

        st.session_state["chat_history"].append({"user": user_question})
        context = assistant.fetch_relevant_context(user_question)
        response = assistant.ai.generate_response(user_question, context)

        st.session_state["chat_history"].append({"bot": response})
        st.write(f"### 🤖 Assistant's Response:\n{response}")

        assistant.visualizer.create_wordcloud(context)

def display_chat_history():
    st.header("📜 Chat History")
    for chat in st.session_state["chat_history"]:
        if "user" in chat:
            st.write(f"**User:** {chat['user']}")
        if "bot" in chat:
            st.write(f"**Bot:** {chat['bot']}")

def main():
    register()

    if not st.session_state["logged_in"]:
        login()
    else:
        st.sidebar.write(f"Logged in as {st.session_state['username']}")
        if st.sidebar.button("Logout"):
            logout()

    if st.session_state["logged_in"]:
        handle_file_upload()
        view_and_delete_documents()
        handle_question_answering()
        display_chat_history()
    else:
        st.info("Please log in to upload documents and ask questions.")

if __name__ == "__main__":
    main()