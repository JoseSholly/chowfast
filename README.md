# ChowFast Backend

A Django REST Framework-based backend API for ChowFast, a food delivery platform that connects customers with vendors.

## Features

- 🔐 **JWT Authentication** - Secure token-based authentication using Simple JWT
- 👥 **Multi-User System** - Support for customers, vendors, and admin users
- 🍔 **Menu Management** - Vendors can manage their menus and items
- 📦 **Order Management** - Complete order processing system
- 💳 **Payment Integration** - Payment processing capabilities
- 📧 **Email Services** - Email functionality powered by Mailgun
- 📚 **API Documentation** - Interactive Swagger/OpenAPI documentation
- 🎨 **Admin Interface** - Beautiful admin panel using Django Jazzmin

## Tech Stack

- **Framework**: Django 5.2.8
- **API**: Django REST Framework 3.16.1
- **Authentication**: Simple JWT 5.5.1
- **Database**: SQLite (development) / PostgreSQL (production)
- **Documentation**: drf-yasg (Swagger/OpenAPI)
- **Email**: Mailgun (via Anymail)
- **Server**: Gunicorn with Uvicorn workers (ASGI)
- **Static Files**: WhiteNoise

## Prerequisites

- Python 3.11+
- pip
- PostgreSQL (for production)
- Virtual environment (recommended)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/JoseSholly/chowfast.git
   cd chowfast_backend
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   cd chowfast_backend
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the `chowfast_backend` directory with the following variables:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DJANGO_SETTINGS_MODULE=chowfast_backend.settings.local
   
   # Database (for production)
   DATABASE_URL=postgresql://user:password@localhost:5432/chowfast_db
   
   # Email Configuration (Mailgun)
   MAILGUN_API_KEY=your-mailgun-api-key
   MAILGUN_DOMAIN_NAME=your-mailgun-domain
   
   # CORS Configuration
   CORS_ALLOWED_ORIGINS=http://localhost:3000
   CSRF_TRUSTED_ORIGINS=http://localhost:3000
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files (for production)**
   ```bash
   python manage.py collectstatic --noinput
   ```

## Running the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access the interactive API documentation:

- **Swagger UI**: `http://localhost:8000/api/swagger/` or `http://localhost:8000/`
- **ReDoc**: `http://localhost:8000/api/redoc/`
## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

