from unittest.mock import patch

from conftest import test_user


def test_get_me(client, get_token):
    with patch("src.services.auth.redis_client") as redis_mock:
        redis_mock.exists.return_value = False
        redis_mock.get.return_value = None
        redis_mock.setex.return_value = True
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("api/users/me", headers=headers)
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["username"] == test_user["username"]
        assert data["email"] == test_user["email"]
        assert "avatar" in data


@patch("src.services.upload_file_service.UploadFileService.upload_file")
def test_update_avatar_user(mock_upload_file, client, get_token):
    with patch("src.services.auth.redis_client") as redis_mock:
        redis_mock.exists.return_value = False
        redis_mock.get.return_value = None
        redis_mock.setex.return_value = True
        fake_url = "http://example.com/avatar.jpg"
        mock_upload_file.return_value = fake_url

        headers = {"Authorization": f"Bearer {get_token}"}

        file_data = {"file": ("avatar.jpg", b"fake image content", "image/jpeg")}

        response = client.patch("/api/users/avatar", headers=headers, files=file_data)

        assert response.status_code == 200, response.text

        data = response.json()
        assert data["username"] == test_user["username"]
        assert data["email"] == test_user["email"]
        assert data["avatar"] == fake_url