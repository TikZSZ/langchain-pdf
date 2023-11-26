from langchain.schema import BaseChatMessageHistory,BaseMessage
from typing import List
from app.web.api import (
    get_messages_by_conversation_id,
    add_message_to_conversation
)

class SQLChatMessageHistory(BaseChatMessageHistory):
  conversation_id:str
  messages:List[BaseMessage] = []

  def __init__(self,conversation_id:str):
    self.conversation_id = conversation_id
    self.messages = get_messages_by_conversation_id(self.conversation_id)

  def add_message(self, message: BaseMessage) -> None:
    content = message.content
    role = message.type
    try:
        add_message_to_conversation(
            conversation_id=self.conversation_id,
            role=role,
            content=content
        )
        self.messages.append(message)
    except:
        print("an error occured while adding the message")
    #add to db and list

  def clear(self):
    pass