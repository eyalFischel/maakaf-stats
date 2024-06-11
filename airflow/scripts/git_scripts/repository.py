from pydantic import BaseModel

class Repository(BaseModel):
    owner: str
    name: str
