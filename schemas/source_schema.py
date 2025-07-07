from pydantic import BaseModel;

class SourceSchema(BaseModel):
    link: str
    description: str