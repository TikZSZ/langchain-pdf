from typing import Any, Optional, Union,Iterator
from queue import Queue
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv
from langchain.schema.output import ChatGenerationChunk, GenerationChunk, LLMResult
from langchain.chains import LLMChain
from threading import Thread
load_dotenv()

chat = ChatOpenAI(
  streaming=True,
)

prompt = ChatPromptTemplate.from_messages([
  ("human","{content}")
])

class StreamingHandler(BaseCallbackHandler):
  queue:Queue
  def __init__(self,queue) -> None:
    super().__init__()
    self.queue = queue
  def on_llm_new_token(self, token: str,chunk:Optional[Union[GenerationChunk, ChatGenerationChunk]],**kwargs ) -> Any:
    self.queue.put(token)
  def on_llm_end(self, response: LLMResult,**kwargs):
    self.queue.put(None)
  def on_llm_error(self, error: BaseException,**kwargs: Any) -> Any:
    self.queue.put(None)

class StreamableChain:
  def stream(
        self,
        input,
        **kwargs: Optional[Any],
  ) -> Iterator:
        queue = Queue()
        handler = StreamingHandler(queue)
        def task():
          self(input,callbacks=[handler],**kwargs)
        thread = Thread(target=task)
        thread.start()
        while True:
          token = queue.get() 
          if token is None:
            break
          yield token

class StreamingChain(StreamableChain,LLMChain):
  pass
        
chain = StreamingChain(llm=chat,prompt=prompt)

messages = prompt.format_messages(content = "tell me a joke")
chain.stream(input={"content":"tell me a joke"})
for token in chain.stream(input={"content":"tell me a joke"}):
  print(token)