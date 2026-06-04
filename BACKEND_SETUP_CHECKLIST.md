# Django Backend Setup Checklist & Infrastructure Summary

## 📋 Setup Checklist

### Phase 0: Prerequisites
- [ ] Python 3.10+ installed
- [ ] PostgreSQL client tools available
- [ ] Git configured
- [ ] Supabase account created
- [ ] Text editor/IDE ready

### Phase 1: Environment Setup
- [ ] Navigate to backend folder: `cd backend/`
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate venv (Linux/Mac: `source venv/bin/activate` | Windows: `venv\Scripts\activate`)
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Verify Django: `django-admin --version` (should be 4.2.13)

### Phase 2: Configuration
- [ ] Copy env template: `cp .env.example .env`
- [ ] Get Supabase credentials from dashboard
- [ ] Edit `.env` with actual values:
  - [ ] DB_HOST (from Supabase)
  - [ ] DB_PASSWORD (from Supabase)
  - [ ] SECRET_KEY (generate or use provided)
  - [ ] CORS_ALLOWED_ORIGINS (for local dev, can keep as is)
- [ ] Verify `.env` is in `.gitignore` (DO NOT commit)

### Phase 3: Database Setup
- [ ] Test Supabase connection: `psql -h YOUR_HOST -U postgres -d postgres`
- [ ] Run migrations: `python manage.py migrate`
- [ ] Check migration output (should show 30+ migrations applied)
- [ ] Verify tables in Supabase:
  ```sql
  SELECT table_name FROM information_schema.tables WHERE table_schema='public';
  ```
  Should see: users, students, employers, opportunities, applications, admin_panel, etc.

### Phase 4: Admin Setup
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Enter credentials (remember these!)
- [ ] Test admin access: http://localhost:8000/admin/

### Phase 5: Server Verification
- [ ] Start dev server: `python manage.py runserver`
- [ ] Wait for message: "Starting development server at http://127.0.0.1:8000/"
- [ ] Test endpoints:
  - [ ] http://localhost:8000/api/v1/docs/ (Swagger UI)
  - [ ] http://localhost:8000/api/v1/redoc/ (ReDoc)
  - [ ] http://localhost:8000/admin/ (Django Admin)

### Phase 6: First API Call
- [ ] Test register endpoint:
  ```bash
  curl -X POST http://localhost:8000/api/v1/auth/register/ \
    -H "Content-Type: application/json" \
    -d '{
      "email": "test@example.com",
      "password": "TestPass123!",
      "password_confirm": "TestPass123!",
      "role": "student"
    }'
  ```
- [ ] Verify response with tokens
- [ ] Copy access token for next test

### Phase 7: Authenticated Endpoint
- [ ] Test current user endpoint:
  ```bash
  curl -X GET http://localhost:8000/api/v1/auth/me/ \
    -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
  ```
- [ ] Verify returns user data

### Phase 8: Create Test Data
- [ ] Create additional test accounts:
  - [ ] 1 student account
  - [ ] 1 employer account
- [ ] Via Django admin or API

---

## 🏗️ Backend Infrastructure Summary

### Project Structure
```
backend/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── setup.sh                     # Automated setup script
│
├── attachlink/                  # Main Django project
│   ├── __init__.py
│   ├── wsgi.py                  # WSGI config (production)
│   ├── urls.py                  # Main URL routing
│   └── settings/
│       ├── base.py              # Base settings (shared)
│       ├── development.py       # Dev settings
│       └── production.py        # Prod settings
│
├── apps/                        # Django applications
│   ├── users/                   # Authentication & users
│   │   ├── models.py            # User, AdminUser models
│   │   ├── views.py             # Auth views (register, login, etc)
│   │   ├── urls.py              # Auth routes
│   │   ├── admin.py             # Admin configuration
│   │   ├── apps.py              # App config
│   │   ├── signals.py           # Signal handlers
│   │   └── migrations/
│   │
│   ├── students/                # Student profiles
│   │   ├── models.py            # StudentProfile model
│   │   ├── views.py             # Profile views
│   │   ├── urls.py              # Routes
│   │   ├── admin.py             # Admin config
│   │   ├── apps.py              # App config
│   │   └── migrations/
│   │
│   ├── employers/               # Employer profiles
│   │   ├── models.py            # Employer model
│   │   ├── views.py             # Profile views
│   │   ├── urls.py              # Routes
│   │   ├── admin.py             # Admin config
│   │   ├── apps.py              # App config
│   │   └── migrations/
│   │
│   ├── opportunities/           # Job postings
│   │   ├── models.py            # Opportunity model
│   │   ├── views.py             # CRUD views
│   │   ├── urls.py              # Routes
│   │   ├── admin.py             # Admin config
│   │   ├── apps.py              # App config
│   │   └── migrations/
│   │
│   ├── applications/            # Job applications
│   │   ├── models.py            # Application model
│   │   ├── views.py             # CRUD views
│   │   ├── urls.py              # Routes
│   │   ├── admin.py             # Admin config
│   │   ├── apps.py              # App config
│   │   └── migrations/
│   │
│   └── admin_panel/             # Admin dashboard
│       ├── models.py            # FlaggedContent, AdminAction models
│       ├── views.py             # Admin views
│       ├── urls.py              # Routes
│       ├── admin.py             # Admin config
│       ├── apps.py              # App config
│       └── migrations/
│
├── utils/                       # Shared utilities
│   ├── __init__.py
│   └── permissions.py           # Custom permission classes
│
├── static/                      # Static files (if needed)
├── media/                       # User uploads
├── logs/                        # Application logs
└── tests/                       # Test files

```

---

## 🔑 Key Configuration Files

### 1. `.env` (Not in repo - create from .env.example)
```env
DEBUG=True
DJANGO_SETTINGS_MODULE=attachlink.settings.development
SECRET_KEY=your-50-char-secret-key
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-supabase-password
DB_HOST=your-project.supabase.co
DB_PORT=5432
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 2. `requirements.txt`
Contains 30+ Python packages:
- Django + DRF + CORS + Filters
- PostgreSQL adapter
- JWT authentication
- Utilities (python-dotenv, Pillow, etc)
- Testing tools (pytest, factory-boy)
- Development tools (black, flake8, isort)

### 3. `manage.py`
Django's command-line utility. Usage:
```bash
python manage.py migrate
python manage.py runserver
python manage.py createsuperuser
python manage.py shell
```

### 4. Settings Modules
- **base.py**: 300+ lines of shared config
- **development.py**: DEBUG=True, lenient CORS, console email
- **production.py**: DEBUG=False, strict security, HTTPS required

---

## 📊 Database Schema Summary

### 8 Main Tables (Auto-created by Django)

1. **users_user** (15 fields)
   - Authentication for all roles
   - Email verification tracking
   
2. **users_adminuser** (5 fields)
   - Admin-specific permissions
   - Moderation statistics

3. **students_studentprofile** (16 fields)
   - Academic & professional info
   - GPA, skills, CV, preferences

4. **employers_employer** (18 fields)
   - Company profiles
   - Verification workflow

5. **opportunities_opportunity** (22 fields)
   - Job postings
   - Auto-status updates

6. **applications_application** (13 fields)
   - Application tracking
   - Status flow & decision

7. **admin_panel_flaggedcontent** (11 fields)
   - Content moderation
   - Audit trail

8. **admin_panel_adminaction** (8 fields)
   - Admin action logging
   - Compliance tracking

Plus 50+ Django system tables for auth, permissions, content type, sessions, etc.

---

## 🔌 API Endpoints Overview

### Authentication (`/api/v1/auth/`)
- `POST /register/` - Create account
- `POST /login/` - Get JWT tokens
- `POST /refresh/` - Refresh token
- `POST /logout/` - Invalidate token
- `GET /me/` - Current user

### Student Profile (`/api/v1/students/`)
- `GET /profile/` - Get own profile
- `PUT /profile/` - Update own profile
- `GET /profile/<id>/` - View student's public profile

### Employer Profile (`/api/v1/employers/`)
- `GET /profile/` - Get own profile
- `PUT /profile/` - Update own profile
- `GET /profile/<id>/` - View employer's public profile

### Opportunities (`/api/v1/opportunities/`)
- `GET /` - List jobs (with filters)
- `POST /create/` - Post new job
- `GET /<id>/` - View job details
- `PUT /<id>/update/` - Edit job
- `POST /<id>/close/` - Close posting

### Applications (`/api/v1/applications/`)
- `GET /` - List my applications
- `POST /apply/` - Submit application
- `GET /<id>/` - View application
- `POST /<id>/withdraw/` - Withdraw app

### Admin (`/api/v1/admin/`)
- `GET /flagged-content/` - List flags
- `POST /flagged-content/<id>/resolve/` - Resolve flag

Plus `/api/v1/docs/` for Swagger UI and `/api/v1/redoc/` for ReDoc

---

## 🔐 Authentication Flow

```
User Registration
   ↓
POST /auth/register/ 
   ↓ (email + password + role)
User Created + Tokens Generated
   ↓ (access + refresh tokens)
Frontend stores tokens in localStorage/cookies

Authenticated Request
   ↓
GET /api/v1/auth/me/
   with Authorization: Bearer ACCESS_TOKEN
   ↓
JWT validated by middleware
   ↓
Returns user data or 401 Unauthorized

Token Expiration
   ↓
POST /api/v1/auth/refresh/
   with refresh token body
   ↓
New access token issued
   ↓
Frontend updates stored token
```

---

## 🧪 Testing Infrastructure

### Test Runner
```bash
pytest
```

### Test Organization
- `tests/` folder (can be expanded)
- Test models, views, serializers, permissions

### Example test command
```bash
pytest tests/ -v --cov=apps
```

---

## 📈 Performance Optimizations

### Database Indexes
- 20+ indexed fields for fast queries
- Compound indexes on common filters
- Foreign key indexes for joins

### Query Optimization
- `select_related()` for FK lookups
- `prefetch_related()` for M2M
- Pagination (default 20 items/page)

### Caching
- Django cache framework configured
- Can use Redis in production

---

## 🚀 Deployment Ready

### Production Deployment
Use settings/production.py with:
- HTTPS only
- Secure cookies
- CORS restrictions
- Real email backend

### Deployment Options
1. **Heroku** - `git push heroku main`
2. **AWS** - EC2 + RDS
3. **DigitalOcean** - App Platform
4. **Render** - Native Django support
5. **PythonAnywhere** - Easy setup

See `DEPLOYMENT.md` for detailed instructions

---

## 📚 Resources

- Django docs: https://docs.djangoproject.com/
- DRF docs: https://www.django-rest-framework.org/
- Supabase docs: https://supabase.com/docs/
- PostgreSQL docs: https://www.postgresql.org/docs/

---

## ✅ Verification Steps

After setup, verify:

1. ✅ `python manage.py check` - No errors
2. ✅ All 8 apps registered in INSTALLED_APPS
3. ✅ All models auto-registered in admin
4. ✅ API docs accessible at `/api/v1/docs/`
5. ✅ Superuser login works
6. ✅ Test registration via API
7. ✅ Database has 58+ tables
8. ✅ No migration warnings

---

**Status**: ✅ Backend infrastructure complete and ready for development!

