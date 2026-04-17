import pytest

from src.services.auth import AuthService
from tests.utils.auth_tokens import build_expired_token


def test_create_and_decode_jwt_token():
    data = {"user_id": 1, "access_level_id": 1}
    encoded_jwt = AuthService().create_access_token(data)

    decoded_jwt = AuthService().decode_access_token(encoded_jwt)

    assert decoded_jwt
    assert decoded_jwt["user_id"] == data["user_id"]
    assert decoded_jwt["access_level_id"] == data["access_level_id"]

@pytest.mark.parametrize(
    "token",
    [None, "this.is.not.a.valid.jwt", build_expired_token()]
)
async def test_me_token_guards_return_401(async_client, token):
    async_client.cookies.clear()
    if token is not None:
        async_client.cookies.set("access_token", token)

    response = await async_client.get("/api/v1/auth/me")
    assert response.status_code == 401
