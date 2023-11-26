from langchain.chains import ConversationalRetrievalChain
from app.chat.chains.streamable import StreamableChain
from app.chat.chains.traceable import TracableChain


class StreamingConversationalRetrievalChain(TracableChain,StreamableChain,ConversationalRetrievalChain):
  pass

