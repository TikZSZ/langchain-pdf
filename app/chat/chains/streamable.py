from app.chat.models import ChatArgs
from typing import Any, Optional, Union,Iterator
from queue import Queue
from app.chat.callbacks.stream import StreamingHandler
from threading import Thread
from flask import current_app

class StreamableChain:
  def stream(
        self,
        input,
        **kwargs: Optional[Any],
  ) -> Iterator:
        queue = Queue()
        handler = StreamingHandler(queue)
        def task(app_context):
          app_context.push()
          self(input,callbacks=[handler],**kwargs)
        thread = Thread(target=task,args=[current_app.app_context()])
        thread.start()
        while True:
          token = queue.get() 
          if token is None:
            break
          yield token