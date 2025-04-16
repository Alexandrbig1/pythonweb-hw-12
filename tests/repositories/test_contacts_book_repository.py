import pytest
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, Mock

from src.entity.models import Contact_Book, User
from src.repositories.contacts_book import ContactBookRepository
from src.schemas.contact_book import ContactBookSchema, ContactBookUpdateSchema

@pytest.fixture
def mock_session():
    session = AsyncMock(spec=AsyncSession)
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.add = Mock()
    session.delete = AsyncMock()
    return session

@pytest.fixture
def contacts_repository(mock_session):
    return ContactBookRepository(mock_session)

@pytest.fixture
def mock_user():
    return User(id=1, username="test_user", email="test@example.com")

@pytest.mark.asyncio
async def test_get_contacts(contacts_repository, mock_session, mock_user):
    # Arrange
    limit = 10
    offset = 0
    mock_contacts = [
        Contact_Book(id=1, name="Contact1", surname="Surname1", email="contact1@test.com", phone="1234567890", date_of_birth=datetime(1990, 1, 1)),
        Contact_Book(id=2, name="Contact2", surname="Surname2", email="contact2@test.com", phone="0987654321", date_of_birth=datetime(1991, 2, 2))
    ]
    mock_result = Mock()
    mock_result.scalars.return_value.all.return_value = mock_contacts
    mock_session.execute.return_value = mock_result

    # Act
    result = await contacts_repository.get_contact(limit, offset, mock_user)

    # Assert
    assert result == mock_contacts
    mock_session.execute.assert_called_once()

@pytest.mark.asyncio
async def test_get_contact_by_id(contacts_repository, mock_session, mock_user):
    # Arrange
    contact_id = 1
    mock_contact = Contact_Book(
        id=contact_id,
        name="Test Contact",
        surname="Test Surname",
        email="contact@test.com",
        phone="1234567890",
        date_of_birth=datetime(1990, 1, 1)
    )
    mock_result = Mock()
    mock_result.scalar_one_or_none.return_value = mock_contact
    mock_session.execute.return_value = mock_result

    # Act
    result = await contacts_repository.get_contact_by_id(contact_id, mock_user)

    # Assert
    assert result == mock_contact
    mock_session.execute.assert_called_once()

@pytest.mark.asyncio
async def test_create_contact(contacts_repository, mock_session, mock_user):
    # Arrange
    contact_data = ContactBookSchema(
        name="New Contact",
        surname="New Surname",
        email="new@test.com",
        phone="1234567890",
        date_of_birth=datetime(1990, 1, 1)
    )
    mock_contact = Contact_Book(
        id=1,
        name=contact_data.name,
        surname=contact_data.surname,
        email=contact_data.email,
        phone=contact_data.phone,
        date_of_birth=contact_data.date_of_birth
    )
    mock_session.refresh.return_value = mock_contact

    # Act
    result = await contacts_repository.create_contact(contact_data, mock_user)

    # Assert
    assert result.name == mock_contact.name
    assert result.surname == mock_contact.surname
    assert result.email == mock_contact.email
    assert result.phone == mock_contact.phone
    assert result.date_of_birth == mock_contact.date_of_birth
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()

@pytest.mark.asyncio
async def test_remove_contact(contacts_repository, mock_session, mock_user):
    # Arrange
    contact_id = 1
    mock_contact = Contact_Book(
        id=contact_id,
        name="Test Contact",
        surname="Test Surname",
        email="contact@test.com",
        phone="1234567890",
        date_of_birth=datetime(1990, 1, 1)
    )
    mock_result = Mock()
    mock_result.scalar_one_or_none.return_value = mock_contact
    mock_session.execute.return_value = mock_result

    # Act
    result = await contacts_repository.remove_contact(contact_id, mock_user)

    # Assert
    assert result == mock_contact
    mock_session.delete.assert_called_once_with(mock_contact)
    mock_session.commit.assert_called_once()

@pytest.mark.asyncio
async def test_remove_contact_not_found(contacts_repository, mock_session, mock_user):
    # Arrange
    contact_id = 999
    mock_result = Mock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_result

    # Act
    result = await contacts_repository.remove_contact(contact_id, mock_user)

    # Assert
    assert result is None
    mock_session.delete.assert_not_called()
    mock_session.commit.assert_not_called()

@pytest.mark.asyncio
async def test_update_contact(contacts_repository, mock_session, mock_user):
    # Arrange
    contact_id = 1
    update_data = ContactBookUpdateSchema(
        name="Updated Contact",
        surname="Updated Surname",
        email="updated@test.com",
        phone="9876543210",
        date_of_birth=datetime(1991, 2, 2)
    )
    mock_contact = Contact_Book(
        id=contact_id,
        name="Old Contact",
        surname="Old Surname",
        email="old@test.com",
        phone="1234567890",
        date_of_birth=datetime(1990, 1, 1)
    )
    mock_result = Mock()
    mock_result.scalar_one_or_none.return_value = mock_contact
    mock_session.execute.return_value = mock_result

    # Act
    result = await contacts_repository.update_contact(contact_id, update_data, mock_user)

    # Assert
    assert result == mock_contact
    assert result.name == update_data.name
    assert result.surname == update_data.surname
    assert result.email == update_data.email
    assert result.phone == update_data.phone
    assert result.date_of_birth == update_data.date_of_birth
    mock_session.commit.assert_called_once()