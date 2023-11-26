import os
from langchain.vectorstores.pinecone import Pinecone
import  pinecone
from app.chat.embeddings.baai_bge import embeddings
from app.chat.models import ChatArgs

pinecone.init(
  api_key=os.getenv("PINECONE_API_KEY"),
  environment=os.getenv("PINECONE_ENV_NAME")
)
vectorstore = Pinecone.from_existing_index(index_name=os.getenv("PINECONE_INDEX_NAME"),embedding=embeddings)


def build_retriver(chat_args:ChatArgs,k:int):
  search_kwargs = {"filter":{"pdf_id":chat_args.pdf_id}}
  return vectorstore.as_retriever(
    search_kwargs=search_kwargs
)
