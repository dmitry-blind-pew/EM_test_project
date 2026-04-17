import pytest


@pytest.mark.parametrize(
    "user_type, user_id, access_level, status_code",
    [
        ("none", "4", "2", 401),
        ("user", "4", "2", 403),
        ("premium", "4", "2", 403),
        ("admin", "4", "2", 200),
    ],
)
async def test_admin_get_change_access_level(user_id, access_level, status_code, async_client, user_type, all_tokens):
    get_user_access_level = await async_client.get(
        "/api/v1/admin/users",
        params={"user_id": user_id},
        cookies={"access_token": all_tokens[user_type]},
    )
    assert get_user_access_level.status_code == status_code
    if status_code != 200:
        return

    change_user_access_level = await async_client.put(
        "/api/v1/admin/users/roles",
        params={"user_id": user_id, "access_level": access_level},
        cookies={"access_token": all_tokens[user_type]},
    )
    assert change_user_access_level.status_code == status_code
    if status_code != 200:
        return


async def test_admin_change_access_level_persists(async_client, all_tokens):
    user_id = "1"
    new_access_level = "2"

    change_user_access_level = await async_client.put(
        "/api/v1/admin/users/roles",
        params={"user_id": user_id, "access_level": new_access_level},
        cookies={"access_token": all_tokens["admin"]},
    )
    assert change_user_access_level.status_code == 200

    get_user_access_level = await async_client.get(
        "/api/v1/admin/users",
        params={"user_id": user_id},
        cookies={"access_token": all_tokens["admin"]},
    )
    assert get_user_access_level.status_code == 200
    payload = get_user_access_level.json()
    assert payload
    assert payload[0]["access_level_id"] == int(new_access_level)
