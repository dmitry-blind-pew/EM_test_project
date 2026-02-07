from src.mappers.base import DataMapper
from src.models import UserAccessLevelsORM
from src.models.auth import UsersORM
from src.schemas.access import UserRegAccessLevelsSchema, UserAccessLevelsPatchSchema
from src.schemas.auth import UserSchema, UserLoginHashedSchema, UserActiveSchema


class UsersMapper(DataMapper):
    db_model = UsersORM
    schema = UserSchema


class UsersActiveMapper(DataMapper):
    db_model = UsersORM
    schema = UserActiveSchema


class UsersMapperHashed(DataMapper):
    db_model = UsersORM
    schema = UserLoginHashedSchema


class UserAccessLevelsMapper(DataMapper):
    db_model = UserAccessLevelsORM
    schema = UserRegAccessLevelsSchema


class UserAccessLevelsPatchMapper(DataMapper):
    db_model = UserAccessLevelsORM
    schema = UserAccessLevelsPatchSchema
