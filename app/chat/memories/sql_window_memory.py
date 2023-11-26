from .histories.sql_history import SQLChatMessageHistory
from app.chat.models import ChatArgs
from langchain.memory import ConversationBufferWindowMemory

def window_buffer_memory_builder(chat_args:ChatArgs,k:int):
  return ConversationBufferWindowMemory(
    chat_memory=SQLChatMessageHistory(
      conversation_id=chat_args.conversation_id,
    ),
    k=k,
    memory_key="chat_history",
    output_key="answer",
    return_messages=True
)

