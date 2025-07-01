from pydantic import BaseModel

class ModelSchema(BaseModel):
    name: str
    version: str