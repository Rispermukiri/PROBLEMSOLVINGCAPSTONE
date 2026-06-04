# 🚀 AttachLink Django Backend

Complete Django REST Framework backend for the AttachLink internship/attachment finder platform.

## ✨ Features

- **User Authentication** - JWT-based auth with role system (student, employer, admin)
- **Student Profiles** - Academic & professional data management
- **Employer Profiles** - Company verification workflow
- **Job Postings** - Opportunity management with auto-status updates
- **Applications** - Student application tracking with status flow
- **Admin Dashboard** - Content moderation and audit logging
- **API Documentation** - Auto-generated Swagger UI & ReDoc
- **PostgreSQL** - Supabase integration ready

## 🏗️ Tech Stack

- **Framework**: Django 4.2.13
- **API**: Django REST Framework 3.14
- **Database**: PostgreSQL via Supabase
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Documentation**: drf-spectacular
- **Testing**: pytest, pytest-django
- **Code Quality**: black, flake8, isort

## 📦 Quick Start

### 1. Setup (Automated)
```bash
cd backend/
bash setup.sh
```

### 2. Setup (Manual)
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Supabase credentials

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver
```

### 3. Access API
- **Swagger Docs**: http://localhost:8000/api/v1/docs/
- **ReDoc**: http://localhost:8000/api/v1/redoc/
- **Admin Panel**: http://localhost:8000/admin/

## 📋 Project Structure

```
backend/
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies (30+ packages)
├── .env.example          # Environment template
├── setup.sh              # Automated setup script
│
├── attachlink/           # Main Django project
│   ├── settings/         # Configuration (base, dev, prod)
│   ├── urls.py           # Main URL routing
│   └── wsgi.py           # Production WSGI
│
└── apps/                 # 6 Core applications
    ├── users/            # Authentication (User, AdminUser)
    ├── students/         # Student profiles
    ├── employers/        # Employer profiles
    ├── opportunities/    # Job postings
    ├── applications/     # Job applications
    └── admin_panel/      # Moderation & audit logs
```

## 🔐 Authentication

### Register
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

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "password": "SecurePass123"
  }'
```

### Use Token
```bash
curl -X GET http://localhost:8000/api/v1/auth/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 📚 Core API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/auth/register/` | Register new user |
| POST | `/auth/login/` | Login user |
| GET | `/auth/me/` | Current user |
| GET | `/students/profile/` | Get student profile |
| PUT | `/students/profile/` | Update student profile |
| GET | `/employers/profile/` | Get employer profile |
| PUT | `/employers/profile/` | Update employer profile |
| GET | `/opportunities/` | List jobs |
| POST | `/opportunities/create/` | Post new job |
| GET | `/opportunities/<id>/` | View job details |
| GET | `/applications/` | List my applications |
| POST | `/applications/apply/` | Apply to job |
| GET | `/admin/flagged-content/` | Moderation queue |

Complete endpoint list available in `/api/v1/docs/`

## 🗄️ Database Models

### User (Authentication)
- Email, password, role (student|employer|admin)
- Email verification tracking
- Account status management

### StudentProfile
- University, major, GPA (0-4.00)
- Skills (JSON array)
- CV upload
- Profile completion tracking

### Employer
- Company details, logo
- Verification workflow
- Ban/suspension support
- Statistics tracking

### Opportunity
- Job title, description, requirements
- Salary range, location, remote option
- Auto-status updates (open→expired)
- Application tracking

### Application
- Links student to opportunity
- Cover letter, CV snapshot
- Status flow: pending→reviewed→accepted/rejected
- Rating and notes

### FlaggedContent & AdminAction
- Content moderation
- Audit logging for compliance
- Resolution tracking

## 🛠️ Database Setup

### Using Supabase

1. Create Supabase project at https://supabase.com/
2. Get credentials from Project Settings → Database
3. Add to `.env`:
   ```env
   DB_HOST=your-project.supabase.co
   DB_USER=postgres
   DB_PASSWORD=your-password
   DB_NAME=postgres
   DB_PORT=5432
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```

### Verify Tables Created
```sql
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';
```

## 📊 Django Admin

Access at http://localhost:8000/admin/ with superuser credentials.

Register your models:
- Users & AdminUsers
- StudentProfiles
- Employers
- Opportunities
- Applications
- FlaggedContent
- AdminActions

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps

# Run specific app
pytest tests/ -v -k "test_register"
```

## 🚀 Development Commands

```bash
# Start development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Access Django shell
python manage.py shell

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Check for issues
python manage.py check
```

## 📁 Configuration Files

### `.env` (Development)
```env
DEBUG=True
DJANGO_SETTINGS_MODULE=attachlink.settings.development
SECRET_KEY=your-secret-key-min-50-chars
DB_HOST=your-project.supabase.co
DB_USER=postgres
DB_PASSWORD=your-password
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Settings Module Flow
```
settings/
├── base.py          ← Base config (300+ lines)
├── development.py   ← DEBUG=True, lenient CORS
└── production.py    ← DEBUG=False, secure
```

## 🔒 Security Considerations

### Development
- DEBUG=True (shows errors)
- CORS allows localhost
- Console email backend

### Production
- DEBUG=False
- Strong SECRET_KEY required
- HTTPS only
- Secure cookies
- Restricted CORS
- Real email backend

See `BACKEND_SETUP_GUIDE.md` for production deployment.

## 📖 Documentation

- **[BACKEND_SETUP_GUIDE.md](../BACKEND_SETUP_GUIDE.md)** - Complete setup instructions
- **[BACKEND_SETUP_CHECKLIST.md](../BACKEND_SETUP_CHECKLIST.md)** - Step-by-step checklist
- **[docs/architecture/](../docs/architecture/)** - Architecture & database design
- **Django Docs**: https://docs.djangoproject.com/
- **DRF Docs**: https://www.django-rest-framework.org/

## 🐛 Troubleshooting

### "psycopg2 connection refused"
```bash
# Check credentials in .env
# Test connection:
psql -h your-host -U postgres -d postgres
```

### "ModuleNotFoundError"
```bash
# Ensure venv is activated and pip install complete
source venv/bin/activate
pip install -r requirements.txt
```

### "Database does not exist"
```bash
# Verify DB_NAME in .env (should be 'postgres')
# Check Supabase dashboard
```

### "Superuser already exists"
```bash
python manage.py changepassword admin
```

## 🔄 Next Steps

- [x] Django project initialized
- [x] 6 apps created with models
- [x] Authentication endpoints
- [x] Core CRUD operations
- [ ] Create DRF serializers (for enhanced API)
- [ ] Add email notifications
- [ ] Implement full-text search
- [ ] Setup CI/CD pipeline
- [ ] Deploy to production

## 📞 Support

- Django Community: https://www.djangoproject.com/
- DRF Community: https://www.django-rest-framework.org/
- Supabase Support: https://supabase.com/docs/

## 📄 License

Part of AttachLink project - Internal use

---

**Last Updated**: June 2026  
**Status**: ✅ Production-ready backend infrastructure  
**Python Version**: 3.10+  
**Django Version**: 4.2.13
