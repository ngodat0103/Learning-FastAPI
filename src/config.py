import os
import re

from pydantic import BaseModel
import yaml


class LLMConfig(BaseModel):
    model: str
    api_key: str
    base_url: str


class MongoConfig(BaseModel):
    mongo_url: str


class ServerConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


## Todo Need a way to load here, not depend in FastAPI
class AppConfig(BaseModel):
    llm: LLMConfig
    mongodb: MongoConfig
    server: ServerConfig


def load_config(config_path: str = "config.yaml") -> AppConfig:
    with open(config_path) as f:
        data = yaml.safe_load(f)
    return AppConfig.model_validate(data)


# custom resolver for ${VAR} and ${VAR:default}
def resolve_env(loader: yaml.Loader, node: yaml.ScalarNode) -> str:
    value = loader.construct_scalar(node)
    pattern = re.compile(r"\$\{(\w+)(?::([^}]*))?}")

    def replacer(match: re.Match) -> str:
        var, default = match.group(1), match.group(2)
        result = os.environ.get(var, default)
        if result is None:
            raise ValueError(
                f"Environment variable '{var}' is not set and has no default"
            )
        return result

    return pattern.sub(replacer, value)


yaml.add_implicit_resolver(
    tag="!env",
    regexp=re.compile(r".*\$\{(\w+)(?::([^}]*))?\}.*"),
    Loader=yaml.SafeLoader,
)
yaml.add_constructor("!env", resolve_env, Loader=yaml.SafeLoader)
