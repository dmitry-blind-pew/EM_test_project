from src.core.config import settings
import logging
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
import jwt
from sqlalchemy.exc import IntegrityError

from src.core.exceptions import UnauthorizedException, UserNotFoundException, UserAlreadyExistsException
from src.schemas.auth import UserRegDataSchema, UserHashDataSchema, UserLogDataSchema, UserShortSchema, UserPatchSchema
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, *, data: dict) -> str:
        """Создает подписанный JWT токен доступа."""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    def hash_password(self, *, password: str) -> str:
        """Хэширует пароль в открытом виде."""
        return self.pwd_context.hash(password)

    def verify_password(self, *, plain_password: str, hashed_password: str) -> bool:
        """Проверяет пароль по хэшу."""
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_access_token(self, *, token: str) -> dict[str, int | str]:
        """Декодирует и валидирует JWT token."""
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.PyJWTError as exc:
            logger.warning("Ошибка декодирования JWT: %s", exc.__class__.__name__)
            raise UnauthorizedException() from exc

    async def login_user(self, *, user_data: UserLogDataSchema) -> str:
        """Аутентифицирует пользователя и возвращает токен доступа."""
        user = await self.db.users.get_user_with_hashed_password(email=user_data.email)
        if user is None or not self.verify_password(plain_password=user_data.password, hashed_password=user.hashed_password):
            logger.warning("Неуспешный логин для email=%s", user_data.email)
            raise UnauthorizedException()
        if not user.is_active:
            logger.warning("Попытка входа деактивированного пользователя user_id=%s", user.id)
            raise UserNotFoundException()
        user_access = await self.db.admin.get_user_access_level_id(user_id=user.id)
        access_token = self.create_access_token(data={"user_id": user.id, "access_level_id": user_access.access_level_id})
        logger.info("Успешный логин user_id=%s", user.id)
        return access_token

    async def register_user(self, *, user_data: UserRegDataSchema) -> None:
        """Регистрирует нового пользователя с базовым уровнем доступа."""
        hashed_password = self.hash_password(password=user_data.password)
        hashed_user_data = UserHashDataSchema(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            hashed_password=hashed_password,
        )
        try:
            user = await self.db.users.add(hashed_user_data)
        except IntegrityError as exc:
            logger.warning("Попытка повторной регистрации email=%s", user_data.email)
            raise UserAlreadyExistsException() from exc
        user_data_access = await self.db.users.get_default_access_level(user_id=user.id)
        await self.db.admin.add(user_data_access)
        await self.db.commit()
        logger.info("Пользователь зарегистрирован user_id=%s", user.id)

    async def get_me(self, *, user_id: int) -> UserShortSchema:
        """Возвращает профиль текущего пользователя."""
        user = await self.db.users.get_one_or_none(id=user_id)
        if user is None:
            raise UnauthorizedException()
        user_short = UserShortSchema(**user.model_dump())
        return user_short

    async def patch_user(self, *, user_id: int, user_data: UserPatchSchema) -> None:
        """Обновляет профиль текущего пользователя."""
        await self.db.users.edit(id=user_id, update_data=user_data, exclude_unset=True)
        await self.db.commit()

    async def delete_user(self, *, user_id: int) -> None:
        """Деактивирует аккаунт текущего пользователя."""
        status = await self.db.users.get_deactivate()
        await self.db.users.edit(id=user_id, update_data=status, exclude_unset=True)
        await self.db.commit()
