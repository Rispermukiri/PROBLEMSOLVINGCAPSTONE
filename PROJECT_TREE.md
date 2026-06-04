# AttachLink - Complete Project Tree

```
PROBLEMSOLVINGCAPSTONE/
│
├── 📁 frontend/                    # React + Tailwind + Vite
│   ├── 📁 src/
│   │   ├── 📁 components/
│   │   │   ├── 📁 common/          # Reusable UI components (Button, Modal, Input, Card, Badge, Alert)
│   │   │   └── 📁 layout/          # Layout wrapper components (Header, Sidebar, Footer, MainLayout)
│   │   │
│   │   ├── 📁 features/            # Feature-based modules (MAIN FEATURE CODE)
│   │   │   ├── 📁 auth/
│   │   │   │   ├── 📁 components/  (LoginForm, RegisterForm, RoleSelector, PasswordReset)
│   │   │   │   ├── 📁 pages/       (LoginPage, RegisterPage, VerifyEmailPage)
│   │   │   │   ├── 📁 hooks/       (useAuth, useLogin)
│   │   │   │   ├── 📁 services/    (authService - API calls)
│   │   │   │   └── index.js        # Feature exports
│   │   │   │
│   │   │   ├── 📁 student/
│   │   │   │   ├── 📁 components/  (StudentCard, ProfileForm, CVUploader, StudentFilters)
│   │   │   │   ├── 📁 pages/       (StudentDashboard, StudentProfile, MyApplications)
│   │   │   │   ├── 📁 services/    (studentService)
│   │   │   │   └── index.js
│   │   │   │
│   │   │   ├── 📁 employer/
│   │   │   │   ├── 📁 components/  (EmployerCard, CompanyForm, ApplicantsList, EmployerFilters)
│   │   │   │   ├── 📁 pages/       (EmployerDashboard, CompanyProfile, ManageApplications)
│   │   │   │   ├── 📁 services/    (employerService)
│   │   │   │   └── index.js
│   │   │   │
│   │   │   ├── 📁 opportunities/
│   │   │   │   ├── 📁 components/  (OpportunityCard, OpportunityForm, SearchBar, FilterPanel)
│   │   │   │   ├── 📁 pages/       (OpportunitiesList, OpportunityDetailPage, CreateOpportunity)
│   │   │   │   ├── 📁 services/    (opportunityService)
│   │   │   │   └── index.js
│   │   │   │
│   │   │   ├── 📁 applications/
│   │   │   │   ├── 📁 components/  (ApplicationCard, ApplicationForm, ApplicationStatus)
│   │   │   │   ├── 📁 pages/       (ApplicationsPage, ApplicationDetail, StudentApplications)
│   │   │   │   ├── 📁 services/    (applicationService)
│   │   │   │   └── index.js
│   │   │   │
│   │   │   └── 📁 admin/
│   │   │       ├── 📁 components/  (UserManagement, EmployerVerification, FlaggedContent, Analytics)
│   │   │       ├── 📁 pages/       (AdminDashboard, UsersPage, ReportsPage)
│   │   │       ├── 📁 services/    (adminService)
│   │   │       └── index.js
│   │   │
│   │   ├── 📁 hooks/               # Global custom hooks (useApi, usePagination, useLocalStorage, useDebounce, useModal)
│   │   ├── 📁 services/            # Global services (api.js - Axios instance with interceptors, constants.js)
│   │   ├── 📁 utils/               # Utilities (validators, formatters, localStorage helpers, errorHandler)
│   │   ├── 📁 context/             # React Context (AuthContext, ThemeContext, NotificationContext)
│   │   ├── 📁 types/               # Type definitions (user.types, opportunity.types, application.types)
│   │   ├── 📁 constants/           # App constants (roles, status, messages)
│   │   ├── 📁 styles/              # Global stylesheets (globals.css, themes.css, animations.css)
│   │   ├── App.jsx                 # Main app with routing & role-based redirects
│   │   └── index.jsx               # React entry point
│   │
│   ├── 📁 public/
│   │   ├── index.html
│   │   ├── logo.svg
│   │   └── 📁 images/              # Static images
│   │
│   ├── .env.example                # Environment variables template
│   ├── .env.local                  # Local env (gitignored)
│   ├── package.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── vite.config.js
│   └── README.md
│
├── 📁 backend/                     # Django REST API
│   ├── 📁 attachlink/              # Django project config
│   │   ├── 📁 settings/
│   │   │   ├── base.py             # Core settings (INSTALLED_APPS, DATABASES, MIDDLEWARE, CORS)
│   │   │   ├── local.py            # Local development overrides
│   │   │   ├── production.py       # Production overrides
│   │   │   └── __init__.py
│   │   ├── urls.py                 # Main URL router
│   │   ├── asgi.py                 # ASGI config
│   │   ├── wsgi.py                 # WSGI config
│   │   └── __init__.py
│   │
│   ├── 📁 apps/                    # Django applications (each app self-contained)
│   │   ├── 📁 users/               # User authentication & base user model
│   │   │   ├── 📁 migrations/
│   │   │   ├── models.py           # User, Role models
│   │   │   ├── views.py            # Registration, login, profile endpoints
│   │   │   ├── serializers.py      # UserSerializer, validation
│   │   │   ├── urls.py
│   │   │   ├── permissions.py      # Role-based permissions classes
│   │   │   ├── authentication.py   # JWT token handling
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── tests.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── 📁 students/            # Student profile management
│   │   │   ├── 📁 migrations/
│   │   │   ├── models.py           # StudentProfile model
│   │   │   ├── views.py            # Student profile endpoints
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── tests.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── 📁 employers/           # Employer profile management
│   │   │   ├── 📁 migrations/
│   │   │   ├── models.py           # Employer, Company models
│   │   │   ├── views.py            # Employer endpoints
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── tests.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── 📁 opportunities/       # Internship opportunity management
│   │   │   ├── 📁 migrations/
│   │   │   ├── models.py           # Opportunity model
│   │   │   ├── views.py            # List, create, update, delete endpoints
│   │   │   ├── serializers.py
│   │   │   ├── filters.py          # Filtering, searching, sorting
│   │   │   ├── urls.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── tests.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── 📁 applications/        # Application tracking
│   │   │   ├── 📁 migrations/
│   │   │   ├── models.py           # Application model
│   │   │   ├── views.py            # Apply, track, update application endpoints
│   │   │   ├── serializers.py
│   │   │   ├── signals.py          # Event handling (status updates, notifications)
│   │   │   ├── urls.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── tests.py
│   │   │   └── __init__.py
│   │   │
│   │   └── 📁 admin_panel/         # Admin management endpoints
│   │       ├── 📁 migrations/
│   │       ├── models.py           # FlaggedContent, AdminAction models
│   │       ├── views.py            # User management, reports, verification
│   │       ├── serializers.py
│   │       ├── urls.py
│   │       ├── admin.py
│   │       ├── apps.py
│   │       ├── tests.py
│   │       └── __init__.py
│   │
│   ├── 📁 utils/                   # Shared utilities & helpers
│   │   ├── validators.py           # Custom validators (email, password, CV format)
│   │   ├── decorators.py           # @require_role, @check_permission, etc.
│   │   ├── exceptions.py           # Custom exceptions (InvalidRole, UploadError)
│   │   ├── pagination.py           # Custom pagination classes
│   │   ├── response.py             # Standardized API response format
│   │   ├── file_handlers.py        # File upload/processing utilities
│   │   ├── email_service.py        # Email sending (verification, notifications)
│   │   ├── notifications.py        # In-app notification logic
│   │   ├── constants.py            # App-wide constants
│   │   └── __init__.py
│   │
│   ├── 📁 tests/                   # Test suite structure
│   │   ├── 📁 users/
│   │   │   ├── test_models.py
│   │   │   ├── test_views.py
│   │   │   ├── test_serializers.py
│   │   │   └── __init__.py
│   │   ├── 📁 students/
│   │   │   ├── test_models.py
│   │   │   ├── test_views.py
│   │   │   └── __init__.py
│   │   ├── 📁 employers/
│   │   │   └── ...
│   │   ├── 📁 opportunities/
│   │   │   └── ...
│   │   ├── 📁 applications/
│   │   │   └── ...
│   │   ├── conftest.py             # Pytest configuration & fixtures
│   │   └── __init__.py
│   │
│   ├── 📁 media/                   # User uploads
│   │   ├── 📁 cvs/                 # Student CVs
│   │   ├── 📁 company_logos/       # Company logos
│   │   └── 📁 profile_pictures/    # User profiles
│   │
│   ├── 📁 static/                  # Compiled static files
│   ├── 📁 logs/                    # Application logs
│   │
│   ├── manage.py                   # Django CLI
│   ├── .env.example
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── pytest.ini
│   ├── .flake8
│   └── README.md
│
├── 📁 docs/                        # Project documentation
│   ├── 📁 api/
│   │   ├── authentication.md       # JWT flow, endpoints
│   │   ├── students.md
│   │   ├── employers.md
│   │   ├── opportunities.md
│   │   ├── applications.md
│   │   ├── admin.md
│   │   └── error_codes.md
│   │
│   ├── 📁 architecture/
│   │   ├── system_design.md        # High-level overview
│   │   ├── database_schema.md      # ER diagram, relationships
│   │   ├── auth_flow.md            # Auth & authorization
│   │   └── deployment.md           # Production setup
│   │
│   └── 📁 guides/
│       ├── SETUP.md                # Local dev setup
│       ├── CONTRIBUTING.md         # Dev guidelines
│       ├── TESTING.md              # Testing instructions
│       └── TROUBLESHOOTING.md      # Common issues
│
├── 📁 .github/
│   └── 📁 workflows/               # CI/CD pipelines
│       ├── frontend-build.yml      # React build & test
│       ├── backend-build.yml       # Python tests
│       ├── docker-build.yml        # Docker image build
│       └── deploy.yml              # Production deploy
│
├── .gitignore
├── README.md                       # Project overview & quick start
├── FOLDER_STRUCTURE.md             # This structure explained
├── PROJECT_TREE.md                 # This file - visual tree
├── docker-compose.yml              # Multi-container orchestration
└── CONTRIBUTION_GUIDELINES.md      # How to contribute
```

---

## Quick Reference: File Purpose Summary

### Frontend Key Files
- `src/App.jsx` → Route definitions, layout setup, role-based redirects
- `src/context/AuthContext.jsx` → Global auth state (current user, token)
- `src/services/api.js` → Axios instance with JWT injection
- `src/features/*/services/` → API calls for each feature
- `tailwind.config.js` → Custom theme colors & styling
- `src/utils/validators.js` → Form validation logic

### Backend Key Files
- `attachlink/settings/base.py` → Core Django config
- `apps/users/models.py` → User model, roles
- `apps/*/serializers.py` → Validation & JSON serialization
- `apps/*/views.py` → API endpoints (ViewSets)
- `utils/permissions.py` → Role-based access control
- `utils/response.py` → Standardized API response format

### Documentation Files
- `FOLDER_STRUCTURE.md` → Why each folder exists (READ THIS FIRST!)
- `docs/api/*.md` → API endpoint documentation
- `docs/architecture/database_schema.md` → Database design
- `docs/guides/SETUP.md` → Dev environment setup

---

## Development Workflow

1. **Pick a Feature** (e.g., "Student Profile Upload")
2. **Backend First**: Create models, serializers, viewsets in `apps/students/`
3. **Write Tests**: Add tests in `tests/students/`
4. **Frontend**: Create components in `features/student/components/`
5. **Connect**: Create service in `features/student/services/` to call backend API
6. **Test & Deploy**: Run all tests, create PR

---

## Key Architecture Decisions

✅ **Frontend**: Feature-based modules + shared utilities
✅ **Backend**: Django apps + centralized utilities
✅ **Testing**: Mirror code structure in tests/
✅ **Documentation**: API docs + Architecture guides + Setup guides
✅ **CI/CD**: GitHub Actions for automated testing & deployment

