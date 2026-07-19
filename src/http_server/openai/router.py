from fastapi import APIRouter
from http_server.openai.schema import OpenAICompatibleChatRequest, ChatCompletionMessage
from fastapi import Depends
from langgraph.checkpoint.mongodb import MongoDBSaver
from core_ai.hello_world_langgraph import HelloWorldGraph
from deps import get_checkpointer

openai_compatible_router = APIRouter()


@openai_compatible_router.post("/chat")
async def chat(
    chat_request: OpenAICompatibleChatRequest,
    mongo_checkpointer: MongoDBSaver = Depends(get_checkpointer),
) -> ChatCompletionMessage:
    messages = chat_request.messages
    helloWorld_Graph = HelloWorldGraph(mongo_checkpointer)
    response = await helloWorld_Graph(message="Hello World", thread_id="random_id")
    return ChatCompletionMessage(name="opus", content=response)
