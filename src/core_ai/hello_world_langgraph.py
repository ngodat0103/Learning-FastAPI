from typing import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.mongodb import MongoDBSaver


class AgentState(TypedDict):
    message: str


class HelloWorldGraph:
    def __init__(self, mongo_checkpointer: MongoDBSaver):
        builder = StateGraph(AgentState)
        builder.add_node("hello", self._hello_node)
        builder.add_node("shout", self._shout_node)
        builder.set_entry_point("hello")
        builder.add_edge("hello", "shout")
        builder.add_edge("shout", END)
        self._graph = builder.compile(checkpointer=mongo_checkpointer)

    def _hello_node(self, state: AgentState) -> AgentState:
        return {"message": f"Hello, {state['message']}!"}

    def _shout_node(self, state: AgentState) -> AgentState:
        return {"message": state["message"].upper()}

    async def __call__(self, message: str, thread_id: str) -> str:
        config = {"configurable": {"thread_id": thread_id}}
        result = await self._graph.ainvoke({"message": message}, config=config)
        return result["message"]
