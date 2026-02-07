from src.services.auth import AuthService


def test_create_and_decode_jwt_token():
    data = {"user_id": 1, "access_level_id": 1}
    encoded_jwt = AuthService().create_access_token(data)

    decoded_jwt = AuthService().decode_access_token(encoded_jwt)

    assert decoded_jwt
    assert decoded_jwt["user_id"] == data["user_id"]
    assert decoded_jwt["access_level_id"] == data["access_level_id"]
