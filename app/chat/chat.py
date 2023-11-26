from app.chat.models import ChatArgs
from app.chat.vectorestores import retriever_map
from app.chat.memories import memory_map
from app.chat.llms import llm_map
from app.chat.chains.c_qa_retrieval_chain import StreamingConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from app.web.api import get_conversation_components,set_conversation_components
from typing import Any
from functools import cache
from app.chat.score import random_componenet_by_score

def _build_chat(chat_args: ChatArgs):
    components = get_conversation_components(chat_args.conversation_id)
    already_exsits = components.get("llm") is not None
    retriever,retriever_name = component_picker("retriever",components,retriever_map,chat_args)
    llm,llm_name = component_picker("llm",components,llm_map,chat_args)
    memory,memory_name = component_picker("memory",components,memory_map,chat_args)
    print(f"Running chain with memory:{memory_name}, llm:{llm_name}, retriever: {retriever_name}")
    if not already_exsits:
        set_conversation_components(
            chat_args.conversation_id,
            llm=llm_name,
            retriever=retriever_name,
            memory=memory_name
        )
    
    condense_question_llm = ChatOpenAI(streaming=False)
    return StreamingConversationalRetrievalChain.from_llm(
        llm=llm,
        memory=memory,
        retriever=retriever,
        condense_question_llm=condense_question_llm,
        metadata=chat_args.metadata
    )

build_chat = cache(_build_chat)

def component_picker(component_type:str,components:dict,component_build_map:dict,chat_args:ChatArgs) -> (Any,str):
    component_key = components[component_type]
    if component_key is None:
        component_key = random_componenet_by_score(component_type,component_build_map)
        print("componenet_key = ",component_key)
    return (component_build_map[component_key](chat_args),component_key)


