from pydantic import BaseModel


class DataAddSchema(BaseModel):
    content: str
    security_level: int
