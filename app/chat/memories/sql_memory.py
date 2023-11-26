from app.chat.models import ChatArgs
from langchain.memory import ConversationBufferMemory
from .histories.sql_history import SQLChatMessageHistory


def build_memory(chat_args:ChatArgs):
    return ConversationBufferMemory(
        chat_memory=SQLChatMessageHistory(conversation_id=chat_args.conversation_id),
        memory_key="chat_history",
        output_key="answer",
        return_messages=True
    )
