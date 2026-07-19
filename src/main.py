from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langgraph.checkpoint.mongodb import MongoDBSaver  # single class, has async methods
from http_server.openai.router import openai_compatible_router
import uvicorn
import config
import os


class AppState:
    checkpointer: MongoDBSaver = None


app_state = AppState()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app_config = config.load_config(os.environ.get("CONFIG_PATH", "config.yaml"))
    with MongoDBSaver.from_conn_string(app_config.mongodb.mongo_url) as checkpointer:
        app_state.checkpointer = checkpointer
        yield  # closes mongo connection on shutdown


def get_checkpointer() -> MongoDBSaver:
    return app_state.checkpointer


app = FastAPI(version="beta", lifespan=lifespan)


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse("/docs")


app.include_router(openai_compatible_router)

if __name__ == "__main__":
    app_config = config.load_config(os.environ.get("CONFIG_PATH", "config.yaml"))
    server_config = app_config.server
    uvicorn.run(app, host=server_config.host, port=server_config.port)
