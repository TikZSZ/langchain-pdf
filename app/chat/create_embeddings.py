from langchain.document_loaders import PyPDFLoader 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.chat.vectorestores.pincone import vectorstore

def create_embeddings_for_pdf(pdf_id: str, pdf_path: str):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    loader = PyPDFLoader(pdf_path)

    docs = loader.load_and_split(text_splitter=text_splitter)
    
    for doc in docs:
        doc.metadata = {
            "pdf_id":pdf_id,
            "text":doc.page_content,
            "page":doc.metadata.get("page")
        }
    vectorstore.add_documents(docs)

