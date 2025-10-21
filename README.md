
<img width="1897" height="1080" alt="image" src="https://github.com/user-attachments/assets/6240b74a-07c5-4484-a81e-3caec1e01f3a" />


# FastAPI Backend - Book Management System

A modern, scalable FastAPI backend application for managing books and users with authentication, Redis caching, and PostgreSQL database integration.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Tech Stack & Dependencies](#tech-stack--dependencies)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Database Setup](#database-setup)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Deployment](#deployment)
- [Contributing](#contributing)

## 🚀 Project Overview

This FastAPI backend provides a comprehensive book management system with the following features:

- **User Management**: Registration, authentication, and role-based access control
- **Book Management**: CRUD operations for books with user associations
- **Authentication**: JWT-based authentication with access and refresh tokens
- **Caching**: Redis integration for session management and caching
- **Database**: PostgreSQL with SQLModel/SQLAlchemy ORM
- **Migrations**: Alembic for database schema management
- **Docker Support**: Containerized deployment with Docker Compose

## 🏗️ Architecture

The application follows a modular, layered architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                      │
├─────────────────────────────────────────────────────────────┤
│  Core Layer                                                 │
│  ├── Database (SQLModel + PostgreSQL)                     │
│  ├── Authentication Guards                                 │
│  ├── Middleware (Logging, CORS, Security)                 │
│  └── Router Management                                     │
├─────────────────────────────────────────────────────────────┤
│  Common Layer                                              │
│  ├── Exception Handling                                    │
│  ├── Response Handlers                                     │
│  ├── Services (JWT, Mail, Redis)                           │
│  ├── Settings Management                                   │
│  └── Utilities                                             │
├─────────────────────────────────────────────────────────────┤
│  Modules Layer                                             │
│  ├── User Module (Models, Controllers, Routes, Schemas)   │
│  └── Book Module (Models, Controllers, Routes, Schemas)   │
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ Tech Stack & Dependencies

### Core Framework
- **FastAPI** - Modern, fast web framework for building APIs with Python
- **Uvicorn** - ASGI server for running FastAPI applications
- **Python 3.8+** - Programming language

### Database & ORM
- **PostgreSQL** - Primary database for data persistence
- **SQLModel** - Modern ORM built on top of SQLAlchemy and Pydantic
- **SQLAlchemy** - SQL toolkit and ORM for Python
- **Alembic** - Database migration tool for SQLAlchemy

### Authentication & Security
- **JWT (JSON Web Tokens)** - For stateless authentication
- **Pydantic** - Data validation and settings management
- **Python-dotenv** - Environment variable management

### Caching & Session Management
- **Redis** - In-memory data structure store for caching and sessions

### Development & Deployment
- **Docker** - Containerization platform
- **Docker Compose** - Multi-container Docker application management

### Additional Packages
- **Pydantic Settings** - Settings management with validation
- **Contextlib** - Context management utilities
- **UUID** - Unique identifier generation
- **Datetime** - Date and time handling

## 📁 Project Structure

```
fastapi-backend/
├── app/                          # Main application directory
│   ├── main.py                   # Application entry point
│   ├── core/                     # Core application components
│   │   ├── database/             # Database configuration
│   │   │   └── main.py           # Database connection setup
│   │   ├── guards/               # Authentication guards
│   │   │   └── auth_guard.py     # JWT authentication guard
│   │   ├── middleware/           # Application middleware
│   │   │   └── loggin.py         # Logging middleware
│   │   └── router/               # Router configuration
│   │       └── root_route.py     # Main router setup
│   ├── common/                   # Shared utilities and services
│   │   ├── exceptions/           # Custom exception handling
│   │   │   ├── __init__.py
│   │   │   └── base.py           # Base exception classes
│   │   ├── handlers/             # Request/response handlers
│   │   │   ├── exception_handler.py
│   │   │   └── response_handler.py
│   │   ├── logger/               # Logging configuration
│   │   │   └── logger.py
│   │   ├── schemas/              # Common schemas
│   │   │   └── main.py
│   │   ├── services/             # Business logic services
│   │   │   ├── jwt_services.py   # JWT token management
│   │   │   ├── mail_service.py   # Email service
│   │   │   └── redis_service.py # Redis client
│   │   ├── settings/             # Application settings
│   │   │   └── main.py           # Settings configuration
│   │   └── utils/                # Utility functions
│   │       ├── cookie_manager.py
│   │       └── datetime.py
│   └── modules/                  # Feature modules
│       ├── user/                 # User management module
│       │   ├── user_controller.py
│       │   ├── user_helper.py
│       │   ├── user_models.py
│       │   ├── user_routes.py
│       │   └── user_schema.py
│       └── book/                 # Book management module
│           ├── book_controller.py
│           ├── book_models.py
│           ├── book_routes.py
│           └── book_schema.py
├── migrations/                   # Database migrations
│   ├── env.py                    # Alembic environment
│   ├── script.py.mako            # Migration template
│   └── versions/                 # Migration files
├── scripts/                      # Utility scripts
├── docker-compose.yml           # Docker Compose configuration
├── Dockerfile                   # Docker image configuration
├── requirements.txt             # Python dependencies
├── alembic.ini                  # Alembic configuration
├── dev.sh                       # Development startup script
└── migrate.sh                   # Database migration script
```

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose
- Git

### 1. Clone the Repository

```bash
git clone <repository-url>
cd fastapi-backend
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```env
# Database Configuration
DATABASE_URL=postgresql+asyncpg://shivam:shivam2003@localhost:5432/fastapi_db

# JWT Configuration
ACCESS_TOKEN_SECRET_KEY=your_access_token_secret_key_here
REFRESH_TOKEN_SECRET_KEY=your_refresh_token_secret_key_here

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=shivam2003

# Email Configuration
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password
MAIL_FROM=your_email@example.com
MAIL_SERVER=smtp.gmail.com
```

## 🗄️ Database Setup

### Using Docker Compose (Recommended)

1. **Start Services**:
```bash
docker-compose up -d
```

This will start:
- PostgreSQL database on port 5432
- Redis server on port 6379

2. **Run Migrations**:
```bash
./migrate.sh
```

### Manual Database Setup

1. **Install PostgreSQL** and create database:
```sql
CREATE DATABASE fastapi_db;
CREATE USER shivam WITH PASSWORD 'shivam2003';
GRANT ALL PRIVILEGES ON DATABASE fastapi_db TO shivam;
```

2. **Install Redis**:
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis
```

3. **Run Migrations**:
```bash
alembic upgrade head
```

## 🚀 Development

### Start Development Server

```bash
./dev.sh
```

Or manually:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: `http://localhost:8000`

### API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Database Migrations

**Create a new migration**:
```bash
alembic revision --autogenerate -m "Description of changes"
```

**Apply migrations**:
```bash
alembic upgrade head
```

**Rollback migration**:
```bash
alembic downgrade -1
```

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Authentication Endpoints

#### User Registration
```http
POST /api/v1/users/register
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword"
}
```

#### User Login
```http
POST /api/v1/users/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword"
}
```

#### Refresh Token
```http
POST /api/v1/users/refresh
Content-Type: application/json

{
  "refresh_token": "your_refresh_token_here"
}
```

### Book Management Endpoints

#### Get All Books
```http
GET /api/v1/books
Authorization: Bearer <access_token>
```

#### Create Book
```http
POST /api/v1/books
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "publisher": "Scribner",
  "page_count": 180,
  "language": "English"
}
```

#### Get Book by ID
```http
GET /api/v1/books/{book_id}
Authorization: Bearer <access_token>
```

#### Update Book
```http
PUT /api/v1/books/{book_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Updated Title",
  "author": "Updated Author"
}
```

#### Delete Book
```http
DELETE /api/v1/books/{book_id}
Authorization: Bearer <access_token>
```

## 🐳 Deployment

### Docker Deployment

1. **Build and Run with Docker Compose**:
```bash
docker-compose up -d --build
```

2. **Production Environment Variables**:
Update the `.env` file with production values:
```env
DATABASE_URL=postgresql+asyncpg://user:password@db_host:5432/production_db
REDIS_HOST=redis_host
REDIS_PASSWORD=production_redis_password
```

### Production Considerations

- Use environment-specific settings
- Configure proper CORS origins
- Set up SSL/TLS certificates
- Use a reverse proxy (nginx)
- Configure proper logging
- Set up monitoring and health checks

## 🔧 Development Scripts

### Available Scripts

- `./dev.sh` - Start development server with hot reload
- `./migrate.sh` - Run database migrations
- `docker-compose up -d` - Start all services with Docker

### Code Quality

The project follows Python best practices:
- Type hints throughout the codebase
- Async/await for database operations
- Proper error handling and logging
- Modular architecture with separation of concerns

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the logs for debugging information

---

**Happy Coding! 🚀**
