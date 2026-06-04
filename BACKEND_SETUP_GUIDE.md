# AttachLink Django Backend Setup Guide

## Overview
This guide walks through setting up the AttachLink Django backend with PostgreSQL via Supabase, JWT authentication, and all required dependencies.

## Prerequisites
- Python 3.10+ installed
- PostgreSQL database (Supabase account recommended)
- pip and virtualenv installed
- Git (for version control)

---

## Step 1: Virtual Environment Setup

### Create virtual environment
```bash
cd backend/
python -m venv venv
```

### Activate virtual environment
**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### Verify activation
```bash
which python  # Linux/Mac
# or
where python  # Windows
```

---

## Step 2: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Expected installation time
- 3-5 minutes depending on internet speed
- Total packages: 30+

### Verify installation
```bash
python -m django --version
# Should output: 4.2.13
```

---

## Step 3: Environment Configuration

### Copy environment template
```bash
cp .env.example .env
```

### Edit .env with your Supabase credentials
```bash
nano .env  # or use your preferred editor
```

### Required environment variables for development:

```env
# Django Configuration
DEBUG=True
DJANGO_SETTINGS_MODULE=attachlink.settings.development
SECRET_KEY=your-super-secret-key-min-50-chars-change-in-prod

# Database (Supabase PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-supabase-password
DB_HOST=your-project.supabase.co
DB_PORT=5432

# CORS (for local development)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# JWT
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

### Get Supabase credentials:
1. Go to https://supabase.com/
2. Create a new project or use existing one
3. Go to **Project Settings** → **Database**
4. Copy connection details:
   - Host: `your-project.supabase.co`
   - User: `postgres`
   - Password: From project creation step
   - Database: `postgres`
   - Port: `5432`

---

## Step 4: Run Django Migrations

### Check migration status
```bash
python manage.py showmigrations
```

### Create initial migrations
```bash
python manage.py makemigrations
```

### Apply migrations
```bash
python manage.py migrate
```

### Expected output:
```
Running migrations:
  Applying admin.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying auth.0002_alter_permission_options... OK
  ...
  Applying users.0001_initial... OK
  Applying students.0001_initial... OK
  Applying employers.0001_initial... OK
  Applying opportunities.0001_initial... OK
  Applying applications.0001_initial... OK
  Applying admin_panel.0001_initial... OK
```

### Verify in Supabase:
- Go to **Dashboard** → **SQL Editor**
- Check if tables exist:
  ```sql
  SELECT table_name FROM information_schema.tables 
  WHERE table_schema = 'public';
  ```

---

## Step 5: Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

### Follow prompts:
```
Username: admin
Email: admin@attachlink.com
Password: [create strong password]
Password (again): [confirm]
```

---

## Step 6: Run Development Server

```bash
python manage.py runserver
```

### Expected output:
```
Django version 4.2.13, using settings 'attachlink.settings.development'
Starting development server at http://127.0.0.1:8000/
```

### Access points:
- **API Docs (Swagger)**: http://localhost:8000/api/v1/docs/
- **API Docs (ReDoc)**: http://localhost:8000/api/v1/redoc/
- **Django Admin**: http://localhost:8000/admin/

---

## Available API Endpoints

### Authentication
- `POST /api/v1/auth/register/` - Register new user
- `POST /api/v1/auth/login/` - Login user
- `POST /api/v1/auth/refresh/` - Refresh JWT token
- `POST /api/v1/auth/logout/` - Logout user
- `GET /api/v1/auth/me/` - Get current user

### Students
- `GET /api/v1/students/profile/` - Get student profile
- `PUT /api/v1/students/profile/` - Update student profile
- `GET /api/v1/students/profile/<id>/` - Get specific student

### Employers
- `GET /api/v1/employers/profile/` - Get employer profile
- `PUT /api/v1/employers/profile/` - Update employer profile
- `GET /api/v1/employers/profile/<id>/` - Get specific employer

### Opportunities
- `GET /api/v1/opportunities/` - List opportunities
- `POST /api/v1/opportunities/create/` - Create opportunity
- `GET /api/v1/opportunities/<id>/` - Get opportunity details
- `PUT /api/v1/opportunities/<id>/update/` - Update opportunity
- `POST /api/v1/opportunities/<id>/close/` - Close opportunity

### Applications
- `GET /api/v1/applications/` - List user applications
- `POST /api/v1/applications/apply/` - Submit application
- `GET /api/v1/applications/<id>/` - Get application details
- `POST /api/v1/applications/<id>/withdraw/` - Withdraw application

### Admin
- `GET /api/v1/admin/flagged-content/` - List flagged content
- `POST /api/v1/admin/flagged-content/<id>/resolve/` - Resolve flag

---

## Database Management

### View all migrations
```bash
python manage.py showmigrations
```

### Create migration for model changes
```bash
python manage.py makemigrations apps.users  # Specific app
```

### Reverse migration (careful!)
```bash
python manage.py migrate apps.users 0001  # Go back to 0001
```

### Drop all tables and reset (BE CAREFUL - LOSES DATA)
```bash
python manage.py migrate apps.users zero  # Revert all
python manage.py migrate  # Reapply
```

---

## Testing the API

### Using curl:

#### Register a student
```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "password": "SecurePass123",
    "password_confirm": "SecurePass123",
    "role": "student"
  }'
```

#### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "password": "SecurePass123"
  }'
```

#### Get current user (with token)
```bash
curl -X GET http://localhost:8000/api/v1/auth/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Using Postman:
1. Install Postman
2. Import collection: [AttachLink Postman Collection](./postman_collection.json)
3. Test endpoints through UI

### Using Python requests:
```python
import requests

BASE_URL = 'http://localhost:8000/api/v1'

# Register
response = requests.post(f'{BASE_URL}/auth/register/', json={
    'email': 'test@example.com',
    'password': 'TestPass123',
    'password_confirm': 'TestPass123',
    'role': 'student'
})
print(response.json())
```

---

## Django Admin Interface

Access at: http://localhost:8000/admin/

### Registered Models:
- Users & Admin Users
- Student Profiles
- Employers
- Opportunities
- Applications
- Flagged Content
- Admin Actions

### Features:
- List, create, edit, delete records
- Filter by status, date, type
- Search by email, company, title
- See related objects

---

## Common Tasks

### Create a student user
```bash
python manage.py shell
```

```python
from apps.users.models import User

user = User.objects.create_user(
    email='student@example.com',
    password='SecurePass123',
    role='student'
)
print(f"Created user: {user.email}")
```

### Create an employer user
```python
user = User.objects.create_user(
    email='employer@company.com',
    password='SecurePass123',
    role='employer'
)
print(f"Created user: {user.email}")
```

### Query students
```python
from apps.students.models import StudentProfile

students = StudentProfile.objects.all()
for student in students:
    print(f"{student.user.email}: GPA {student.gpa}")
```

### Query opportunities
```python
from apps.opportunities.models import Opportunity

opps = Opportunity.objects.filter(is_deleted=False, status='open')
for opp in opps:
    print(f"{opp.title} @ {opp.employer.company_name}")
```

---

## Troubleshooting

### "psycopg2 connection refused"
- Verify Supabase credentials in .env
- Check internet connection
- Test connection: `psql -h your-host -U postgres -d postgres`

### "ModuleNotFoundError"
- Ensure venv is activated
- Run `pip install -r requirements.txt` again

### "Database does not exist"
- Verify DB_NAME in .env (should be 'postgres')
- Check Supabase dashboard for database

### "Superuser already exists"
- Use `python manage.py changepassword admin` to reset password

### "Port 8000 already in use"
- Use different port: `python manage.py runserver 8001`

---

## Next Steps

1. ✅ Backend is running
2. ⏭️ Initialize React frontend
3. ⏭️ Connect frontend to backend API
4. ⏭️ Create DRF serializers for better API responses
5. ⏭️ Add email notifications
6. ⏭️ Set up CI/CD pipeline
7. ⏭️ Deploy to production

---

## Useful Commands

```bash
# Check Python/Django version
python --version
django-admin --version

# Collect static files
python manage.py collectstatic --noinput

# Run tests
pytest

# Format code
black .

# Check code quality
flake8

# Run linting
isort .

# Create Django app (rarely needed)
python manage.py startapp new_app apps/new_app

# Access Django shell
python manage.py shell

# Flush database (CAUTION - loses all data)
python manage.py flush
```

---

## Security Notes

⚠️ **For Development Only:**
- DEBUG=True (exposes error details)
- SECRET_KEY stored in .env (not ideal)
- CORS allows localhost only

✅ **For Production:**
- Change DEBUG=False
- Use strong SECRET_KEY (generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- Use settings/production.py
- Enable HTTPS only
- Use environment variables from secure source
- Set secure cookies

---

## Production Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for:
- Heroku deployment
- AWS deployment
- DigitalOcean deployment
- Gunicorn/Nginx setup

---

## Support

- Django Docs: https://docs.djangoproject.com/
- DRF Docs: https://www.django-rest-framework.org/
- Supabase Docs: https://supabase.com/docs/

---

**Last Updated**: June 2026
**Django Version**: 4.2.13
**Python Version**: 3.10+
