import pytest
from fastapi import HTTPException


async def test_logout_revokes_access_to_me(auth_async_client):
    logout_response = await auth_async_client.post("/api/v1/auth/logout")
    assert logout_response.status_code == 200

    me_response = await auth_async_client.get("/api/v1/auth/me")
    assert me_response.status_code == 401


@pytest.mark.parametrize(
    "email, password, expected_status",
    [
        ("user@example.com", "wrong-password", 401),
        ("unknown@example.com", "any-password", 401),
        ("user@example.com", "", 401),
    ],
)
async def test_login_invalid_credentials_returns_error(async_client, email, password, expected_status):
    response = await async_client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert response.status_code == expected_status


async def test_login_inactive_user_rejected(async_client):
    email = "inactive_user@example.com"
    password = "qwerty123"

    register_response = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": password,
            "first_name": "Inactive",
            "password_repeat": password,
        },
    )
    assert register_response.status_code == 200

    login_response = await async_client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert login_response.status_code == 200

    delete_response = await async_client.delete("/api/v1/auth/me")
    assert delete_response.status_code == 200

    relogin_response = await async_client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert relogin_response.status_code == 404


@pytest.mark.parametrize(
    "email, password, first_name, pass_copy, status_code",
    [
        ("test@gmail.ru", "qwerty", "Dmitry", "qwerty", 200),
        ("test@gmail.ru", "qwerty", "Dmitry", "qwerty", 400),
        ("test@email.com", "1234", "Oleg", "1234", 200),
        ("test@email.com", "1234", "Oleg", "4321", 400),
        ("", "1234", "Dmitry", "1234", 422),
        ("testyahoo.ru", "1234", "Dmitry", "1234", 422),
    ],
)
async def test_auth_reg_login_me_logout(
    email, password, first_name, pass_copy, status_code, async_client
):
    register_user = await async_client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "first_name": first_name, "password_repeat": pass_copy},
    )

    assert register_user.status_code == status_code
    if status_code != 200:
        return

    login_user = await async_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password, "first_name": first_name, "password_repeat": pass_copy},
    )
    assert login_user.status_code == status_code
    user_token = login_user.cookies["access_token"]
    assert user_token is not None

    user_me = await async_client.get("/api/v1/auth/me")
    user_me_dict = user_me.json()
    assert user_me.status_code == status_code
    assert user_me_dict["email"] == email

    logout_user = await async_client.post("/api/v1/auth/logout")
    assert logout_user.status_code == status_code
    try:
        none_user = await async_client.get("/api/v1/auth/me")
    except HTTPException(422):
        assert none_user.status_code == 422
