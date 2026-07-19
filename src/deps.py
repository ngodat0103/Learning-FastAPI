# src/deps.py
from langgraph.checkpoint.mongodb import MongoDBSaver


class AppState:
    checkpointer: MongoDBSaver = None


app_state = AppState()


def get_checkpointer() -> MongoDBSaver:
    return app_state.checkpointer
