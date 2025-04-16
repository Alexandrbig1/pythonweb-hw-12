# pythonweb-hw-12

---

## Project Overview

This project is a **REST API for managing contacts**, built using the **FastAPI** framework. It provides functionality to store and manage contact information, including CRUD operations (Create, Read, Update, Delete). The API uses **SQLAlchemy** as the ORM for database interactions and **PostgreSQL** as the database.

The project now includes **user authentication and authorization** using **JWT tokens**, **email verification**, **rate limiting**, **user avatar management** with **Cloudinary**, **Sphinx documentation**, **Redis caching**, and **password reset functionality**.

---

## Features

- **FastAPI Framework**: A modern, fast (high-performance) web framework for building APIs.
- **SQLAlchemy ORM**: Used for database modeling and interaction.
- **PostgreSQL Database**: A robust and reliable relational database.
- **JWT Authentication**: Secure user authentication and authorization using access tokens.
- **Email Verification**: Users must verify their email addresses to activate their accounts.
- **Rate Limiting**: Limits the number of requests to sensitive routes (e.g., `/me`).
- **User-Specific Operations**: Users can only access and modify their own contacts.
- **CORS Support**: Enabled for secure cross-origin requests.
- **Cloudinary Integration**: Allows users to upload and update their avatars.
- **Sphinx Documentation**: Automatically generated documentation for the application.
- **Redis Caching**: Caches the current user during authentication to reduce database queries.
- **Password Reset**: Allows users to reset their passwords via email.
- **Role-Based Access Control**: Implements roles (`user` and `admin`) to restrict access to certain features.
- **Unit and Integration Testing**: Comprehensive test coverage using `pytest` and `pytest-cov`.

---

## New Features in Homework 12

### 1. **Sphinx Documentation**

- Added Sphinx-generated documentation for the application.
- Docstrings were added to all major modules, classes, and methods.
- Documentation can be built and viewed locally using Sphinx.

### 2. **Unit Testing**

- Repository modules are covered with unit tests using `pytest`.
- Mocked database sessions are used to test repository logic.

### 3. **Integration Testing**

- API routes are covered with integration tests using `pytest`.
- Tests ensure that endpoints behave as expected with real data.

### 4. **Test Coverage**

- Achieved over 75% test coverage for the application.
- Used `pytest-cov` to measure and report test coverage.

### 5. **Redis Caching**

- Implemented caching for the current user during authentication.
- The `get_current_user` function retrieves the user from Redis instead of querying the database.

### 6. **Password Reset**

- Added functionality for users to reset their passwords via email.
- Users receive a password reset link with a token that expires after a set time.

### 7. **Role-Based Access Control**

- Implemented roles (`user` and `admin`) for users.
- Only administrators can change their default avatars.

---

## Requirements

- **Python**: 3.10 or higher
- **PostgreSQL**: Version 14 or higher
- **Redis**: For caching user data.
- **Docker Compose**: For running the application and its dependencies.
- **Dependencies**: Listed in `requirements.txt`

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Alexandrbig1/pythonweb-hw-12.git
   cd pythonweb-hw-12
   ```
2. **Set Up a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set Up the Database**:

- Ensure PostgreSQL is installed and running.
- Create a database named `contacts_db`:

```bash
CREATE DATABASE contacts_db;
```

- Update the `.env` file with your database credentials:

```properties
POSTGRES_DB=contacts_db
POSTGRES_USER=example_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

5. **Set Up Redis**:
   - Ensure Redis is installed and running.
   - Update the .env file with your Redis URL:
   ```bash
   REDIS_URL=redis://localhost
   ```
6. **Run Alembic Migrations**:
   ```bash
   alembic upgrade head
   ```
7. **Start the Application**:

   ```bash
   uvicorn main:app --reload
   ```

8. **Run with Docker Compose** (Optional):
   If you prefer to use Docker Compose, ensure `docker` and `docker-compose` are installed, then run:
   ```bash
   docker-compose up --build
   ```

---

## API Endpoints

### Base URL

```bash
http://localhost:8000
```

### Endpoints

| Method | Endpoint         | Description                           |
| ------ | ---------------- | ------------------------------------- |
| POST   | `/auth/register` | Register a new user                   |
| POST   | `/auth/login`    | Log in and retrieve a JWT token       |
| GET    | `/auth/verify`   | Verify a user's email address         |
| GET    | `/contacts`      | Retrieve all contacts (user-specific) |
| GET    | `/contacts/{id}` | Retrieve a contact by ID              |
| POST   | `/contacts`      | Create a new contact                  |
| PUT    | `/contacts/{id}` | Update a contact by ID                |
| DELETE | `/contacts/{id}` | Delete a contact by ID                |
| GET    | `/me`            | Retrieve the current user's profile   |
| PUT    | `/me/avatar`     | Update the user's avatar              |

### Swagger Documentation

Access the Swagger UI for API documentation at:

```bash
http://localhost:8000/docs
```

---

## Project Structure

```markdown
pythonweb-hw-12/
├── docs/ # Sphinx documentation
├── migrations/ # Alembic migrations
├── src/
│ ├── conf/ # Configuration files
│ ├── database/ # Database session management
│ ├── entity/ # SQLAlchemy models
│ ├── repository/ # Database query logic
│ ├── routes/ # API routes
│ ├── schemas/ # Pydantic schemas
│ ├── services/ # Business logic and service layer
├── main.py # Application entry point
├── .env # Environment variables
├── requirements.txt # Python dependencies
└── README.md # Project documentation
```

---

## Technologies Used

- **FastAPI**: Web framework for building APIs.
- **SQLAlchemy**: ORM for database modeling and interaction.
- **PostgreSQL**: Relational database.
- **Redis**: For caching user data.
- **Pydantic**: Data validation and settings management.
- **Alembic**: Database migrations.
- **Uvicorn**: ASGI server for running the application.
- **JWT**: Secure user authentication and authorization.
- **Cloudinary**: For managing user avatars.
- **Sphinx**: For generating project documentation.
- **Docker Compose**: For containerized deployment.

---

## Environment Variables

All sensitive data is stored in the `.env` file. Example:

```properties
POSTGRES_DB=contacts_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ALGORITHM=HS256
SECRET_KEY=your_secret_key
REDIS_URL=redis://localhost

MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_password
MAIL_FROM=your_email@example.com
MAIL_PORT=465

CLOUDINARY_NAME=your_cloudinary_name
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret
```

---
