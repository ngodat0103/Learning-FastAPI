from pydantic import BaseModel
from typing import List, Union, TypeAlias, TypedDict, Required, Literal
from openai.types.chat import ChatCompletionUserMessageParam


class AssistantMessage(TypedDict):
    role: Required[Literal["assistant"]]
    content: str
    name: str


SimplifiedChatCompletionMessageParam: TypeAlias = Union[
    ChatCompletionUserMessageParam,
    AssistantMessage,
]


class OpenAICompatibleChatRequest(BaseModel):
    messages: List[SimplifiedChatCompletionMessageParam]
    model_config = {
        "json_schema_extra": {
            "example": {
                "messages": [
                    {"role": "user", "content": "What is the capital of France?", "name": "Akira"},
                    {"role": "assistant", "content": "The capital of France is Paris.", "name": "Bot"},
                    {"role": "user", "content": "Thanks!", "name": "Akira"}
                ]
            }
        }
    }