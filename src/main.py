from fastapi import FastAPI
from http_server.openai.router import openai_compatible_router
import uvicorn
import config
import os
from fastapi.responses import RedirectResponse

if __name__ == "__main__":
    app_config = config.load_config(os.environ.get("CONFIG_PATH", "config.yaml"))  # renamed
    server_config = app_config.server  # use app_config here
    app = FastAPI(version="beta")
    @app.get("/",include_in_schema=False)
    async def redirect_to_docs():
        return RedirectResponse("/docs")
    app.include_router(openai_compatible_router)
    uvicorn.run(app, host=server_config.host, port=server_config.port)