from typing import TypedDict
from langgraph.graph import StateGraph, END


# --- State: the "message" passed between nodes ---
# Think of this as your shared JobExecutionContext / Spring Batch JobParameters
class AgentState(TypedDict):
    message: str


# --- Nodes: pure functions that receive state and return a partial update ---
# Analogous to a Tasklet — takes context, returns updated context
def hello_node(state: AgentState) -> AgentState:
    return {"message": f"Hello, {state['message']}!"}


def shout_node(state: AgentState) -> AgentState:
    return {"message": state["message"].upper()}


# --- Graph assembly: analogous to JobBuilderFactory.get("job").start(step1).next(step2) ---
builder = StateGraph(AgentState)

builder.add_node("hello", hello_node)
builder.add_node("shout", shout_node)

builder.set_entry_point("hello")  # first node to execute
builder.add_edge("hello", "shout")  # hello → shout
builder.add_edge("shout", END)  # shout → terminal

graph = builder.compile()

# --- Invoke ---
result = graph.invoke({"message": "World"})
print(result["message"])  # HELLO, WORLD!
