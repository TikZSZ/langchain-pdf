from pydantic import BaseModel, Extra
from hashlib import sha256

class Metadata(BaseModel, extra=Extra.allow):
    conversation_id: str
    user_id: str
    pdf_id: str


class ChatArgs(BaseModel, extra=Extra.allow):
    conversation_id: str
    pdf_id: str
    metadata: Metadata
    streaming: bool

    def __hash__(self):
        hash_string = f"{self.conversation_id}-{self.pdf_id}-{self.streaming}"
        return int(sha256(hash_string.encode('utf-8')).hexdigest(), 16)
