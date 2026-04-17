import jwt
from datetime import datetime, timedelta, timezone

from src.core.config import settings


def build_expired_token() -> str:
    """Формирует просроченный JWT токен доступа."""
    expired_payload = {
        "user_id": 1,
        "access_level_id": 1,
        "exp": datetime.now(timezone.utc) - timedelta(minutes=5),
    }
    return jwt.encode(
        expired_payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
