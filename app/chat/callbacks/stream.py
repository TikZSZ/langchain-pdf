from typing import Any, Dict, List, Optional
from uuid import UUID
from langchain.callbacks.base import BaseCallbackHandler
from queue import Queue
from langchain.schema.messages import BaseMessage
from langchain.schema.output import LLMResult
class StreamingHandler(BaseCallbackHandler):
  queue:Queue
  def __init__(self,queue):
    super().__init__()
    self.queue = queue
    self.streaming_run_id = ""
  def on_chat_model_start(self, serialized: Dict[str, Any],messages,run_id,**kwargs):
    if(serialized["kwargs"]["streaming"]):
      self.streaming_run_id = run_id
  def on_llm_new_token(self, token: str,run_id,**kwargs ):
    if(self.should_access_que(run_id)):
      self.queue.put(token)
  def on_llm_end(self,response,run_id: UUID,**kwargs):
    if(self.should_access_que(run_id)):
      self.queue.put(None)
      self.streaming_run_id = ""
  def on_llm_error(self, error: BaseException,run_id,**kwargs):
    if(self.should_access_que(run_id)):
      self.queue.put(None)
  def should_access_que(self,run_id):
    return self.streaming_run_id == run_id
   
