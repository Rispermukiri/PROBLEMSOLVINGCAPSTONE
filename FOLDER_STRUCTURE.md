# AttachLink - Complete Folder Structure

## Project Overview
AttachLink is a production-grade internship and attachment finder platform built with React (frontend) and Django (backend), following scalable industry standards and best practices.

---

## Root Level Structure

```
PROBLEMSOLVINGCAPSTONE/
├── frontend/              # React application
├── backend/               # Django REST API
├── docs/                  # Project documentation
├── .github/               # GitHub CI/CD workflows
├── .gitignore
├── README.md
├── FOLDER_STRUCTURE.md    # This file
└── docker-compose.yml     # Multi-container orchestration
```

---

## FRONTEND STRUCTURE (`/frontend`)

### Overview
The frontend follows a **feature-based architecture** combined with **utility/shared organization**. This approach:
- Scales well as features grow
- Allows independent feature teams
- Keeps related code together (components, services, hooks, types)
- Separates shared/common utilities for reusability

### Directory Breakdown

```
frontend/
├── src/
│   ├── components/
│   │   ├── common/          # Reusable UI components shared across app
│   │   │   ├── Button.jsx
│   │   │   ├── Card.jsx
│   │   │   ├── Modal.jsx
│   │   │   ├── Input.jsx
│   │   │   ├── Badge.jsx
│   │   │   └── Alert.jsx
│   │   │
│   │   └── layout/          # Layout components (wrapper components)
│   │       ├── Header.jsx
│   │       ├── Sidebar.jsx
│   │       ├── Footer.jsx
│   │       └── MainLayout.jsx
│   │
│   ├── features/            # Feature-based modules (each with own logic)
│   │   ├── auth/            # Authentication feature
│   │   │   ├── components/
│   │   │   │   ├── LoginForm.jsx
│   │   │   │   ├── RegisterForm.jsx
│   │   │   │   ├── RoleSelector.jsx
│   │   │   │   └── PasswordReset.jsx
│   │   │   ├── pages/
│   │   │   │   ├── LoginPage.jsx
│   │   │   │   ├── RegisterPage.jsx
│   │   │   │   └── VerifyEmailPage.jsx
│   │   │   ├── hooks/
│   │   │   │   ├── useAuth.js      # Auth state & methods
│   │   │   │   └── useLogin.js
│   │   │   ├── services/
│   │   │   │   └── authService.js  # API calls for auth
│   │   │   └── index.js            # Feature exports
│   │   │
│   │   ├── student/         # Student-specific feature
│   │   │   ├── components/
│   │   │   │   ├── StudentCard.jsx
│   │   │   │   ├── ProfileForm.jsx
│   │   │   │   ├── CVUploader.jsx
│   │   │   │   └── StudentFilters.jsx
│   │   │   ├── pages/
│   │   │   │   ├── StudentDashboard.jsx
│   │   │   │   ├── StudentProfile.jsx
│   │   │   │   └── MyApplications.jsx
│   │   │   ├── services/
│   │   │   │   └── studentService.js
│   │   │   └── index.js
│   │   │
│   │   ├── employer/        # Employer-specific feature
│   │   │   ├── components/
│   │   │   │   ├── EmployerCard.jsx
│   │   │   │   ├── CompanyForm.jsx
│   │   │   │   ├── ApplicantsList.jsx
│   │   │   │   └── EmployerFilters.jsx
│   │   │   ├── pages/
│   │   │   │   ├── EmployerDashboard.jsx
│   │   │   │   ├── CompanyProfile.jsx
│   │   │   │   └── ManageApplications.jsx
│   │   │   ├── services/
│   │   │   │   └── employerService.js
│   │   │   └── index.js
│   │   │
│   │   ├── opportunities/   # Opportunities listing & browsing
│   │   │   ├── components/
│   │   │   │   ├── OpportunityCard.jsx
│   │   │   │   ├── OpportunityForm.jsx
│   │   │   │   ├── SearchBar.jsx
│   │   │   │   ├── FilterPanel.jsx
│   │   │   │   └── OpportunityDetail.jsx
│   │   │   ├── pages/
│   │   │   │   ├── OpportunitiesList.jsx
│   │   │   │   ├── OpportunityDetailPage.jsx
│   │   │   │   └── CreateOpportunity.jsx
│   │   │   ├── services/
│   │   │   │   └── opportunityService.js
│   │   │   └── index.js
│   │   │
│   │   ├── applications/    # Application management
│   │   │   ├── components/
│   │   │   │   ├── ApplicationCard.jsx
│   │   │   │   ├── ApplicationForm.jsx
│   │   │   │   ├── ApplicationStatus.jsx
│   │   │   │   └── ApplicantReview.jsx
│   │   │   ├── pages/
│   │   │   │   ├── ApplicationsPage.jsx
│   │   │   │   ├── ApplicationDetail.jsx
│   │   │   │   └── StudentApplications.jsx
│   │   │   ├── services/
│   │   │   │   └── applicationService.js
│   │   │   └── index.js
│   │   │
│   │   └── admin/           # Admin-specific feature
│   │       ├── components/
│   │       │   ├── UserManagement.jsx
│   │       │   ├── EmployerVerification.jsx
│   │       │   ├── FlaggedContent.jsx
│   │       │   └── Analytics.jsx
│   │       ├── pages/
│   │       │   ├── AdminDashboard.jsx
│   │       │   ├── UsersPage.jsx
│   │       │   └── ReportsPage.jsx
│   │       ├── services/
│   │       │   └── adminService.js
│   │       └── index.js
│   │
│   ├── hooks/               # Global/shared custom hooks
│   │   ├── useApi.js        # API request handling hook
│   │   ├── usePagination.js
│   │   ├── useLocalStorage.js
│   │   ├── useDebounce.js
│   │   └── useModal.js
│   │
│   ├── services/            # Global API services
│   │   ├── api.js           # Axios instance with interceptors
│   │   └── constants.js     # API endpoints
│   │
│   ├── utils/               # Utility functions
│   │   ├── validators.js    # Input validation
│   │   ├── formatters.js    # Format dates, numbers, etc.
│   │   ├── localStorage.js  # Local storage helpers
│   │   └── errorHandler.js  # Error handling utilities
│   │
│   ├── context/             # React Context for state management
│   │   ├── AuthContext.jsx
│   │   ├── ThemeContext.jsx
│   │   └── NotificationContext.jsx
│   │
│   ├── types/               # TypeScript/JSDoc type definitions
│   │   ├── user.types.js
│   │   ├── opportunity.types.js
│   │   └── application.types.js
│   │
│   ├── constants/           # App-wide constants
│   │   ├── roles.js         # User roles
│   │   ├── status.js        # Application statuses
│   │   └── messages.js      # UI messages
│   │
│   ├── styles/              # Global styles (Tailwind config)
│   │   ├── globals.css
│   │   ├── themes.css
│   │   └── animations.css
│   │
│   ├── App.jsx              # Main App component with routing
│   └── index.jsx            # React entry point
│
├── public/
│   ├── index.html
│   ├── logo.svg
│   └── images/              # Static images
│       ├── hero.jpg
│       ├── placeholder.jpg
│       └── ...
│
├── .env.example             # Environment variables template
├── .env.local               # Local environment (in .gitignore)
├── package.json
├── tailwind.config.js       # Tailwind CSS configuration
├── postcss.config.js
├── vite.config.js           # Vite configuration (if using Vite)
└── README.md
```

### Frontend Key Files Explanation

| File/Folder | Purpose |
|-------------|---------|
| `src/App.jsx` | Route definitions, main layout, role-based redirects |
| `src/context/*` | Global state (auth user, theme, notifications) |
| `src/services/api.js` | Axios instance with JWT token injection, error interceptors |
| `src/hooks/useAuth.js` | Custom hook for authentication logic |
| `src/utils/validators.js` | Email, password, CV file validation |
| `tailwind.config.js` | Custom colors, fonts, breakpoints |
| `src/features/*/services/` | Feature-specific API calls |
| `src/components/common/` | Reusable components (Button, Modal, etc.) |

---

## BACKEND STRUCTURE (`/backend`)

### Overview
The backend follows Django's **app-based architecture** with separation of concerns:
- Each app owns its models, views, serializers, and tests
- Utilities are centralized for shared logic
- Clear separation between business logic and configuration
- Follows Django REST Framework best practices

### Directory Breakdown

```
backend/
├── attachlink/              # Project-level configuration (Django project)
│   ├── settings/
│   │   ├── base.py          # Base settings (databases, apps, middleware)
│   │   ├── local.py         # Local development settings
│   │   ├── production.py    # Production settings
│   │   └── __init__.py
│   ├── urls.py              # Main URL router
│   ├── asgi.py              # ASGI config (production server)
│   └── wsgi.py              # WSGI config (production server)
│
├── apps/                    # Django applications
│   ├── users/               # User authentication & base user model
│   │   ├── migrations/      # Database migration files
│   │   ├── models.py        # User, Role models
│   │   ├── views.py         # User registration, login endpoints
│   │   ├── serializers.py   # User serializers and validation
│   │   ├── urls.py          # User-related URLs
│   │   ├── permissions.py   # Role-based permissions
│   │   ├── authentication.py # JWT token handling
│   │   ├── admin.py         # Django admin config
│   │   ├── apps.py
│   │   ├── tests.py
│   │   └── __init__.py
│   │
│   ├── students/            # Student-specific models & logic
│   │   ├── migrations/
│   │   ├── models.py        # StudentProfile model
│   │   ├── views.py         # Student profile endpoints
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── tests.py
│   │   └── __init__.py
│   │
│   ├── employers/           # Employer-specific models & logic
│   │   ├── migrations/
│   │   ├── models.py        # Employer, Company models
│   │   ├── views.py         # Employer profile endpoints
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── tests.py
│   │   └── __init__.py
│   │
│   ├── opportunities/       # Internship opportunities
│   │   ├── migrations/
│   │   ├── models.py        # Opportunity model
│   │   ├── views.py         # List, create, update opportunities
│   │   ├── serializers.py
│   │   ├── filters.py       # DRF filtering, searching
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── tests.py
│   │   └── __init__.py
│   │
│   ├── applications/        # Student applications for opportunities
│   │   ├── migrations/
│   │   ├── models.py        # Application model
│   │   ├── views.py         # Apply, track, manage applications
│   │   ├── serializers.py
│   │   ├── signals.py       # Event handling (status updates)
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── tests.py
│   │   └── __init__.py
│   │
│   └── admin_panel/         # Admin-specific endpoints
│       ├── migrations/
│       ├── models.py        # FlaggedContent, AdminAction models
│       ├── views.py         # User management, reports
│       ├── serializers.py
│       ├── urls.py
│       ├── admin.py
│       ├── apps.py
│       ├── tests.py
│       └── __init__.py
│
├── utils/                   # Shared utilities & helpers
│   ├── validators.py        # Custom validators (CV format, etc.)
│   ├── decorators.py        # Custom decorators (@require_role, etc.)
│   ├── exceptions.py        # Custom exceptions
│   ├── pagination.py        # Custom pagination
│   ├── response.py          # Standardized API responses
│   ├── file_handlers.py     # File upload/processing
│   ├── email_service.py     # Email sending
│   ├── notifications.py     # Notification logic
│   ├── __init__.py
│   └── constants.py         # App constants
│
├── tests/                   # Test suite structure
│   ├── users/
│   │   ├── test_models.py
│   │   ├── test_views.py
│   │   ├── test_serializers.py
│   │   └── __init__.py
│   ├── students/
│   │   ├── test_models.py
│   │   ├── test_views.py
│   │   └── __init__.py
│   ├── employers/
│   │   └── ...
│   ├── opportunities/
│   │   └── ...
│   ├── applications/
│   │   └── ...
│   └── conftest.py          # Pytest configuration & fixtures
│
├── media/                   # User-uploaded files
│   ├── cvs/                 # Student CVs
│   ├── company_logos/       # Company logos
│   └── profile_pictures/    # User profile pictures
│
├── static/                  # Static files (compiled CSS, JS)
├── logs/                    # Application logs
│
├── manage.py                # Django CLI
├── .env.example             # Environment variables template
├── requirements.txt         # Python dependencies
├── requirements-dev.txt     # Development dependencies
├── pytest.ini               # Pytest configuration
├── .flake8                  # Code style configuration
├── docker-compose.yml       # Multi-container setup
└── README.md
```

### Backend Key Files Explanation

| File/Folder | Purpose |
|-------------|---------|
| `attachlink/settings/base.py` | Core Django settings: INSTALLED_APPS, DATABASES, MIDDLEWARE, CORS config |
| `apps/*/models.py` | Database tables for each feature |
| `apps/*/serializers.py` | Validation and serialization of data to/from JSON |
| `apps/*/views.py` | API endpoints (ViewSets, APIViews) |
| `utils/permissions.py` | Custom permission classes (IsStudent, IsEmployer, etc.) |
| `utils/validators.py` | Email validation, CV format checking, password strength |
| `utils/response.py` | Standardized JSON response structure |
| `media/` | User uploads (CVs, company logos) |
| `tests/` | Unit and integration tests |

---

## DOCUMENTATION STRUCTURE (`/docs`)

```
docs/
├── api/
│   ├── authentication.md    # JWT token flow, login/register endpoints
│   ├── students.md          # Student endpoints
│   ├── employers.md         # Employer endpoints
│   ├── opportunities.md     # Opportunity CRUD endpoints
│   ├── applications.md      # Application endpoints
│   ├── admin.md             # Admin endpoints
│   └── error_codes.md       # API error responses
│
├── architecture/
│   ├── system_design.md     # High-level architecture overview
│   ├── database_schema.md   # ER diagram, table relationships
│   ├── auth_flow.md         # Authentication & authorization flow
│   └── deployment.md        # Docker, production setup
│
└── guides/
    ├── SETUP.md             # Local development setup
    ├── CONTRIBUTING.md      # Development guidelines
    ├── TESTING.md           # How to run tests
    └── TROUBLESHOOTING.md   # Common issues & solutions
```

---

## CI/CD WORKFLOWS (`/.github/workflows`)

```
.github/workflows/
├── frontend-build.yml       # Build & test React on push
├── backend-build.yml        # Run Django tests on push
├── docker-build.yml         # Build Docker images
└── deploy.yml               # Deploy to production
```

---

## Top-Level Config Files

| File | Purpose |
|------|---------|
| `.gitignore` | Python cache, node_modules, .env, db files |
| `README.md` | Project overview, quick start guide |
| `docker-compose.yml` | Multi-container orchestration (Frontend, Backend, Database) |
| `FOLDER_STRUCTURE.md` | This document |

---

## Why This Structure?

### ✅ Scalability
- **Feature-based**: Easy to add new features without reshuffling existing code
- **App-based (Django)**: Clear separation means teams can work in parallel
- **Isolated services**: Each app owns its logic

### ✅ Maintainability
- **Co-location**: Related code lives together (services, components, hooks)
- **Clear concerns**: Business logic separate from views/serializers
- **Tests mirror structure**: Easy to find and write tests

### ✅ Reusability
- `common/` components and `utils/` functions prevent duplication
- Shared hooks and services in dedicated directories
- Global constants centralized

### ✅ Performance
- Code splitting by feature in frontend
- Lazy loading routes
- Clear migration path for shared state

### ✅ Industry Best Practices
- Follows React Hooks patterns and feature-based architecture
- Follows Django REST Framework conventions
- Clear role-based access control structure
- Test-first structure (tests mirror code structure)

---

## Next Steps

1. **Initialize Frontend**: `npm create vite@latest frontend -- --template react`
2. **Initialize Backend**: Django project setup with virtual environment
3. **Create Database Models**: Start with `apps/users/models.py`
4. **Build Authentication**: User registration, JWT tokens
5. **Implement Features**: One feature at a time (student → opportunities → applications)
6. **Add Tests**: As you build each feature

