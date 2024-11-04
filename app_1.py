import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import requests
from bs4 import BeautifulSoup

# Function to process PDFs
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Function to scrape and process web data
def get_web_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    text = "\n".join([para.get_text() for para in paragraphs])
    return text

# Function to split text into chunks for embeddings
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

# Function to create vector store with embeddings
def get_vectorstore(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

# Function to handle user input for question answering
def handle_userinput(question):
    response = st.session_state.conversation({"question": question})
    st.session_state.chat_history = response['chat_history']
    st.write(response)  # Display the answer from the response

# Function to create a conversation chain
def get_conversation_chain(vectorstore):
    llm = ChatGoogleGenerativeAI(model='gemini-1.5-pro-latest')
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

# Main function to run the Streamlit app
def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with PDFs & Web Data", page_icon=":books:")

    # Initialize session states for conversation and chat history
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    # Header and user input for questions
    st.header("Chat with PDFs & Web Data :books:")
    user_question = st.text_input("Ask a question about your documents or web data:")

    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your Documents")
        
        # Upload PDFs
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        
        # Enter URL for web scraping
        url = st.text_input("Enter a URL to scrape")

        if st.button("Process"):
            with st.spinner("Processing..."):
                # Initialize empty raw text
                raw_text = ""
                
                # Process PDF text if uploaded
                if pdf_docs:
                    raw_text += get_pdf_text(pdf_docs)
                
                # Process web text if URL is provided
                if url:
                    web_text = get_web_text(url)
                    raw_text += web_text
                
                # Convert to text chunks
                text_chunks = get_text_chunks(raw_text)
                st.write("Text Chunks:", text_chunks)
                
                # Create vector store
                vectorstore = get_vectorstore(text_chunks)
                
                # Create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)

if __name__ == "__main__":
    main()
