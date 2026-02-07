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
        "/admin/users",
        params={"user_id": user_id},
        cookies={"access_token": all_tokens[user_type]},
    )
    assert get_user_access_level.status_code == status_code
    if status_code != 200:
        return

    change_user_access_level = await async_client.put(
        "/admin/users/roles",
        params={"user_id": user_id, "access_level": access_level},
        cookies={"access_token": all_tokens[user_type]},
    )
    assert change_user_access_level.status_code == status_code
    if status_code != 200:
        return
