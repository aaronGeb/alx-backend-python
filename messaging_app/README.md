# Messaging App

A Django REST Framework-based messaging application that provides real-time chat functionality with user management and conversation handling.

## 📁 Project Structure

```
messaging_app/
├── chats/                          # Main Django app for chat functionality
│   ├── __init__.py
│   ├── admin.py                    # Django admin configuration
│   ├── apps.py                     # App configuration
│   ├── models.py                   # Database models (User, Conversation, Message)
│   ├── serializers.py              # DRF serializers for API responses
│   ├── views.py                    # API view sets and endpoints
│   ├── urls.py                     # URL routing for the chats app
│   ├── tests.py                    # Unit tests
│   └── migrations/                 # Database migration files
│       ├── __init__.py
│       └── 0001_initial.py
├── messaging_app/                  # Django project settings
│   ├── __init__.py
│   ├── settings.py                 # Project configuration
│   ├── urls.py                     # Main URL configuration
│   ├── wsgi.py                     # WSGI configuration
│   └── asgi.py                     # ASGI configuration
├── db.sqlite3                      # SQLite database file
├── manage.py                       # Django management script
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🚀 Features

- **User Management**: Custom user model with role-based access (admin, user, guest)
- **Conversations**: Create and manage group conversations with multiple participants
- **Messaging**: Send and receive messages within conversations
- **Authentication**: Session and Basic authentication support
- **API Endpoints**: RESTful API with proper permissions and filtering
- **Search**: Search conversations by participant details and messages by content
- **Ordering**: Sort messages by timestamp

## 🛠️ Technology Stack

- **Backend**: Django 4.2.24
- **API Framework**: Django REST Framework 3.16.1
- **Database**: SQLite (development), MySQL (production ready)
- **Authentication**: Django's built-in authentication system
- **Environment Management**: django-environ

## 📋 Prerequisites

- Python 3.8+
- pip (Python package installer)
- Virtual environment (recommended)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/aaronGeb/alx-backend-python/tree/main/messaging_app
   cd messaging_app
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/api/v1/`

## 📚 API Documentation

### Base URL
```
http://127.0.0.1:8000/api/v1/
```

### Authentication
The API uses Django's session authentication and basic authentication. Include credentials in your requests:

**Session Authentication**: Login via `/api-auth/login/` and use session cookies
**Basic Authentication**: Include `Authorization: Basic <base64-encoded-credentials>` header

### Endpoints

#### Users
- **GET** `/api/v1/users/` - List all users (admin only)
- **POST** `/api/v1/users/` - Create a new user
- **GET** `/api/v1/users/{id}/` - Get user details
- **PUT/PATCH** `/api/v1/users/{id}/` - Update user
- **DELETE** `/api/v1/users/{id}/` - Delete user

#### Conversations
- **GET** `/api/v1/conversations/` - List user's conversations
- **POST** `/api/v1/conversations/` - Create a new conversation
- **GET** `/api/v1/conversations/{id}/` - Get conversation details
- **PUT/PATCH** `/api/v1/conversations/{id}/` - Update conversation
- **DELETE** `/api/v1/conversations/{id}/` - Delete conversation

#### Messages
- **GET** `/api/v1/messages/` - List messages (filter by conversation)
- **POST** `/api/v1/messages/` - Send a new message
- **GET** `/api/v1/messages/{id}/` - Get message details
- **PUT/PATCH** `/api/v1/messages/{id}/` - Update message
- **DELETE** `/api/v1/messages/{id}/` - Delete message

### Query Parameters

#### Conversations
- `search` - Search by participant email, first name, or last name
- `ordering` - Order by any field (e.g., `created_at`, `-created_at`)

#### Messages
- `conversation` - Filter messages by conversation ID
- `search` - Search by message content
- `ordering` - Order by `sent_at` (e.g., `sent_at`, `-sent_at`)

### Example API Usage

#### Create a User
```bash
curl -X POST http://127.0.0.1:8000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "role": "user"
  }'
```

#### Create a Conversation
```bash
curl -X POST http://127.0.0.1:8000/api/v1/conversations/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic <base64-credentials>" \
  -d '{
    "participants": ["user-uuid-1", "user-uuid-2"]
  }'
```

#### Send a Message
```bash
curl -X POST http://127.0.0.1:8000/api/v1/messages/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic <base64-credentials>" \
  -d '{
    "conversation": "conversation-uuid",
    "message_body": "Hello, how are you?"
  }'
```

## 🗄️ Database Models

### User Model
- `user_id` (UUID, Primary Key)
- `first_name` (CharField, 30 chars)
- `last_name` (CharField, 30 chars)
- `email` (EmailField, unique)
- `password_hash` (CharField, 128 chars)
- `phone_number` (CharField, 15 chars, optional)
- `role` (CharField, choices: admin/user/guest)
- `created_at` (DateTimeField, auto-generated)
- `is_active` (BooleanField)
- `is_staff` (BooleanField)

### Conversation Model
- `conversation_id` (UUID, Primary Key)
- `participants` (ManyToManyField to User)
- `created_at` (DateTimeField, auto-generated)

### Message Model
- `message_id` (UUID, Primary Key)
- `sender` (ForeignKey to User)
- `conversation` (ForeignKey to Conversation)
- `message_body` (TextField, max 1000 chars)
- `sent_at` (DateTimeField, auto-generated)

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

## 🔒 Security Features

- Password hashing using Django's built-in password hashers
- CSRF protection enabled
- Session-based authentication
- Permission-based access control
- Input validation and sanitization
- SQL injection protection through Django ORM

## 🚀 Deployment

For production deployment:

1. Set `DEBUG=False` in your environment variables
2. Configure a production database (MySQL/PostgreSQL)
3. Set up proper secret key management
4. Configure static file serving
5. Set up HTTPS
6. Configure proper logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is part of the ALX Backend Python curriculum.

## 👥 Authors

- **Aaron** - *Initial work* - [GitHub](https://github.com/aarongeb)

## 📞 Support

If you encounter any issues or have questions, please open an issue in the repository.