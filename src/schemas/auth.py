from pydantic import BaseModel, EmailStr, field_validator

from src.exceptions import BadRequestException


class UserSchema(BaseModel):
    id: int
    first_name: str
    last_name: str | None = None
    email: EmailStr
    hashed_password: str


class UserLogDataSchema(BaseModel):
    email: EmailStr
    password: str


class UserRegDataSchema(UserLogDataSchema):
    first_name: str
    last_name: str | None = None
    password_repeat: str

    @field_validator("password_repeat")
    @classmethod
    def check_copy_password(cls, repeat_pass, info):
        orig_pass = info.data.get("password")
        if repeat_pass != orig_pass:
            raise BadRequestException()
        return repeat_pass

    model_config = {"exclude": {"password_repeat"}}


class UserHashDataSchema(BaseModel):
    first_name: str
    last_name: str | None = None
    email: EmailStr
    hashed_password: str


class UserShortSchema(BaseModel):
    first_name: str
    last_name: str | None = None
    email: EmailStr


class UserPatchSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None


class UserActiveSchema(BaseModel):
    is_active: bool


class UserLoginHashedSchema(UserActiveSchema):
    id: int
    hashed_password: str
