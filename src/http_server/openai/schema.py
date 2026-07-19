from pydantic import BaseModel
from typing import List, Union, TypeAlias, TypedDict, Required, Literal, Optional
from openai.types.chat import ChatCompletionUserMessageParam


class AssistantMessage(TypedDict):
    role: Required[Literal["assistant"]]
    content: str
    name: str


SimplifiedChatCompletionMessageParam: TypeAlias = Union[
    ChatCompletionUserMessageParam,
    AssistantMessage,
]

class ChatCompletionMessage(BaseModel):
    name: str
    content: Optional[str] = None
    model_config = {
        "json_schema_extra": {
            "example": {
                "role": "assistant",
                "name": "opus4.8",
                "content": "The capital of France is Paris."
            }
        }
    }
class OpenAICompatibleChatRequest(BaseModel):
    messages: List[SimplifiedChatCompletionMessageParam]
    model_config = {
        "json_schema_extra": {
            "example": {
                "messages": [
                    {"role": "user", "content": "What is the capital of France?", "name": "Akira"},
                    {"role": "assistant", "content": "The capital of France is Paris.", "name": "Bot"},
                    {"role": "user", "content": "Thanks! in behalf of Akira", "name": "Bob"}
                ]
            }
        }
    }