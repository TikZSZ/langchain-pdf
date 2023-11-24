from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5",model_kwargs = {'device': 'cuda'},encode_kwargs = {'normalize_embeddings': True})