from pydantic import BaseModel, EmailStr, ValidationInfo, field_validator

from src.core.exceptions import BadRequestException


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
    def validate_password_repeat(cls, repeat_pass: str, info: ValidationInfo) -> str:
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
