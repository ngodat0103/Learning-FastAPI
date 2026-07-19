from fastapi import APIRouter
from http_server.openai.schema import OpenAICompatibleChatRequest, ChatCompletionMessage

openai_compatible_router = APIRouter()


@openai_compatible_router.post("/chat")
async def chat(chat_request: OpenAICompatibleChatRequest) -> ChatCompletionMessage:
    # Todo interact with real langgraph operation here
    return ChatCompletionMessage(name="opus",content="Dummy reply")