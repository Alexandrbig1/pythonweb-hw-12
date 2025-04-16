from datetime import datetime
from unittest.mock import patch, Mock

import pytest
from sqlalchemy import select

from src.entity.models import Contact_Book
from conftest import TestingSessionLocal

contact_data = {
    "name": "John",
    "surname": "Doe",
    "email": "john.doe@example.com",
    "phone": "1234567890",
    "date_of_birth": "1990-01-01T00:00:00"
}

def test_create_contact(client, get_token):
    with patch("src.services.auth.redis_client") as redis_mock:
        redis_mock.exists.return_value = False
        redis_mock.get.return_value = None
        headers = {"Authorization": f"Bearer {get_token}"}
        response = client.post("api/contacts", json=contact_data, headers=headers)
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["name"] == contact_data["name"]
        assert data["surname"] == contact_data["surname"]
        assert data["email"] == contact_data["email"]
        assert data["phone"] == contact_data["phone"]
        assert "id" in data
        assert "date_of_birth" in data

def test_get_contacts(client, get_token):
    with patch("src.services.auth.redis_client") as redis_mock:
        redis_mock.exists.return_value = False
        redis_mock.get.return_value = None
        headers = {"Authorization": f"Bearer {get_token}"}
        response = client.get("api/contacts", headers=headers)
        assert response.status_code == 200, response.text
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert "id" in data[0]
            assert "name" in data[0]
            assert "surname" in data[0]
            assert "email" in data[0]
            assert "phone" in data[0]
            assert "date_of_birth" in data[0]

@pytest.mark.asyncio
async def test_get_contact_by_id(client, get_token):
    async with TestingSessionLocal() as session:
        # First create a contact to ensure we have one
        contact = Contact_Book(
            name=contact_data["name"],
            surname=contact_data["surname"],
            email=contact_data["email"],
            phone=contact_data["phone"],
            date_of_birth=datetime.fromisoformat(contact_data["date_of_birth"]),
            user_id=1  # Assuming test user has ID 1
        )
        session.add(contact)
        await session.commit()
        await session.refresh(contact)

    with patch("src.services.auth.redis_client") as redis_mock:
        redis_mock.exists.return_value = False
        redis_mock.get.return_value = None
        headers = {"Authorization": f"Bearer {get_token}"}
        response = client.get(f"api/contacts/{contact.id}", headers=headers)
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["id"] == contact.id
        assert data["name"] == contact.name
        assert data["surname"] == contact.surname
        assert data["email"] == contact.email
        assert data["phone"] == contact.phone
        assert "date_of_birth" in data

def test_get_contact_not_found(client, get_token):
    with patch("src.services.auth.redis_client") as redis_mock:
        redis_mock.exists.return_value = False
        redis_mock.get.return_value = None
        headers = {"Authorization": f"Bearer {get_token}"}
        response = client.get("api/contacts/999999", headers=headers)
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Contact not found"

def test_update_contact(client, get_token):
    with patch("src.services.auth.redis_client") as redis_mock:
        redis_mock.exists.return_value = False
        redis_mock.get.return_value = None
        headers = {"Authorization": f"Bearer {get_token}"}
        
        # First create a contact
        response = client.post("api/contacts", json=contact_data, headers=headers)
        assert response.status_code == 201
        contact_id = response.json()["id"]

        # Update the contact
        update_data = {
            "name": "Jane",
            "surname": "Smith",
            "email": "jane.smith@example.com",
            "phone": "0987654321",
            "date_of_birth": "1991-02-02T00:00:00"
        }
        response = client.put(f"api/contacts/{contact_id}", json=update_data, headers=headers)
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["surname"] == update_data["surname"]
        assert data["email"] == update_data["email"]
        assert data["phone"] == update_data["phone"]
        assert "date_of_birth" in data

def test_delete_contact(client, get_token):
    with patch("src.services.auth.redis_client") as redis_mock:
        redis_mock.exists.return_value = False
        redis_mock.get.return_value = None
        headers = {"Authorization": f"Bearer {get_token}"}
        
        # First create a contact
        response = client.post("api/contacts", json=contact_data, headers=headers)
        assert response.status_code == 201
        contact_id = response.json()["id"]

        # Delete the contact
        response = client.delete(f"api/contacts/{contact_id}", headers=headers)
        assert response.status_code == 204

        # Verify contact is deleted
        response = client.get(f"api/contacts/{contact_id}", headers=headers)
        assert response.status_code == 404

def test_unauthorized_access(client):
    # Try to access contacts without token
    response = client.get("api/contacts")
    assert response.status_code == 401, response.text
    
    # Try to create contact without token
    response = client.post("api/contacts", json=contact_data)
    assert response.status_code == 401, response.text
    
    # Try to update contact without token
    response = client.put("api/contacts/1", json=contact_data)
    assert response.status_code == 401, response.text
    
    # Try to delete contact without token
    response = client.delete("api/contacts/1")
    assert response.status_code == 401, response.text