from pydantic_settings import BaseSettings
from pydantic import BaseModel


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080


class ApiPrefix(BaseModel):
    prefix: str = "/api"


class Setting(BaseSettings):
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()


settings = Setting()

