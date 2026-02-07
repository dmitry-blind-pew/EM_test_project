from pydantic import BaseModel


class UserRegAccessLevelsSchema(BaseModel):
    user_id: int
    access_level_id: int


class UserAccessLevelsPatchSchema(BaseModel):
    access_level_id: int


class AccessLevelsSchema(BaseModel):
    id: int
    name: str
