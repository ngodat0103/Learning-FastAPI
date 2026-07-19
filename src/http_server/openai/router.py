from fastapi import FastAPI, APIRouter
from openai.types.chat import ChatCompletion, ChatCompletionMessage
from openai.types.chat.chat_completion import Choice
from openai.types.completion_usage import CompletionUsage
import time

from http_server.openai.schema import OpenAICompatibleChatRequest

openai_compatible_router = APIRouter()


@openai_compatible_router.post("/chat")
async def chat(chat_request: OpenAICompatibleChatRequest):
    return ChatCompletion(
        id="chatcmpl-dummy123",
        object="chat.completion",
        created=int(time.time()),
        model="gpt-3.5-turbo",
        choices=[
            Choice(
                index=0,
                finish_reason="stop",
                message=ChatCompletionMessage(
                    role="assistant",
                    content=f"Dummy reply to: fdsfd"
                )
            )
        ],
        usage=CompletionUsage(
            prompt_tokens=10,
            completion_tokens=20,
            total_tokens=30
        )
    )