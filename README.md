# DocuQueryAI-Emphasizes-document-querying-with-AI.


**DocuQueryAI** is an interactive Streamlit application that lets you chat with your PDF documents and web content. Powered by Google Generative AI, FAISS, and LangChain, this app processes, scrapes, and retrieves relevant data, making it easy to find answers from large text documents and web pages.

## Features

- **PDF Processing**: Upload multiple PDFs, extract, and prepare them for natural language queries.
- **Web Scraping**: Input URLs to retrieve and process web content directly.
- **Conversational AI**: Ask questions about your documents or web data and receive relevant answers with conversational memory.
- **Vector Store with FAISS**: Efficient retrieval of document information using FAISS for text embeddings.

## Tech Stack

- **Streamlit**: UI and app framework.
- **PyPDF2**: PDF text extraction.
- **BeautifulSoup**: Web scraping.
- **Google Generative AI**: Embedding and conversational models.
- **FAISS**: Vector store for efficient information retrieval.
- **LangChain**: Manages conversational chains with memory for a smooth interactive experience.

## Installation

1. **Clone the repository**
   ```bash
   [git clone https://github.com/bharatnokhawal/DocuQueryAI.git](https://github.com/bharatnokhawal/DocuQueryAI-Emphasizes-document-querying-with-AI..git)
   cd DocuQueryAI

   pip install -r requirements.txt


   GOOGLE_API_KEY=your_google_api_key


   streamlit run app_1.py






