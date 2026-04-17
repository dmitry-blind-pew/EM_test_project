import pytest

from src.core.exceptions import UnauthorizedException
from src.services.auth import AuthService
from tests.utils.auth_tokens import build_expired_token


def test_create_access_token():
    """Проверяет, что access token успешно создается."""
    data = {"user_id": 1}
    encoded_jwt = AuthService().create_access_token(data=data)

    assert encoded_jwt
    assert isinstance(encoded_jwt, str)


@pytest.mark.parametrize(
    "token",
    ["this.is.not.a.valid.jwt", build_expired_token()],
)
def test_decode_access_token_raises_unauthorized(token):
    """Проверяет выброс ошибки для невалидного/просроченного token."""
    with pytest.raises(UnauthorizedException):
        AuthService().decode_access_token(token=token)


def test_verify_password_returns_false_for_wrong_password():
    """Проверяет, что неверный пароль не проходит валидацию."""
    auth_service = AuthService()
    hashed_password = auth_service.hash_password(password="correct_password")

    assert auth_service.verify_password(plain_password="wrong_password", hashed_password=hashed_password) is False
