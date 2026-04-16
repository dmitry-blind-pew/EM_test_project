import pytest


@pytest.mark.parametrize(
    "user_type, data_id, content, access_level, status_code_1, status_code_2",
    [
        ("none", "1", "new_data", "2", 401, 401),
        ("none", "2", "new_data", "2", 401, 401),
        ("user", "1", "new_data", "2", 200, 403),
        ("user", "2", "new_data", "2", 403, 403),
        ("premium", "1", "new_data", "2", 200, 403),
        ("premium", "2", "new_data", "2", 200, 403),
        ("admin", "1", "new_data", "2", 200, 200),
        ("admin", "2", "new_data", "2", 200, 200),
    ],
)
async def test_admin_get_change_access_level(
    user_type, data_id, content, access_level, status_code_1, status_code_2, async_client, all_tokens
):
    get_data = await async_client.get(
        f"/data/{data_id}",
        cookies={"access_token": all_tokens[user_type]},
    )
    assert get_data.status_code == status_code_1
    if status_code_1 != 200:
        return

    create_data = await async_client.post(
        "/data",
        params={"content": content, "access_level": access_level},
        cookies={"access_token": all_tokens[user_type]},
    )
    assert create_data.status_code == status_code_2
    if status_code_2 != 200:
        return
