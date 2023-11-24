from app.chat.models import ChatArgs
from app.chat.vectorestores.pincone import build_retriver
from app.chat.memories.sql_chat_message_history import build_memory
from app.chat.llms.chatopenai import build_llm
from app.chat.chains.c_qa_retrieval_chain import StreamingConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

chain_store = {}

def build_chat(chat_args: ChatArgs):
    retriver = build_retriver(chat_args)
    llm = build_llm(chat_args)
    condense_question_llm = ChatOpenAI(streaming=False)
    memory = build_memory(chat_args)
    chain = chain_store.get(f"{chat_args.conversation_id}-{chat_args.pdf_id}")
    if chain:
        return chain
    chain = StreamingConversationalRetrievalChain.from_llm(
        llm=llm,
        memory=memory,
        retriever=retriver,
        condense_question_llm=condense_question_llm,
        verbose=True
    )
    chain_store[f"{chat_args.conversation_id}-{chat_args.pdf_id}"] = chain
    return chain
