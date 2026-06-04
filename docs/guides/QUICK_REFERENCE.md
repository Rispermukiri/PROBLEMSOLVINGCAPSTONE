# AttachLink - Key Files Quick Reference

## Frontend Key Files at a Glance

### Core Application Files

| File | Purpose | Key Content |
|------|---------|-------------|
| `src/App.jsx` | Main app component | Routes, layout, role-based redirects |
| `src/index.jsx` | React entry point | ReactDOM.render, AuthProvider wrapper |
| `src/services/api.js` | Axios instance | JWT injection, error handling interceptors |
| `src/constants/roles.js` | User roles constants | USER_ROLES.STUDENT, USER_ROLES.EMPLOYER |
| `src/context/AuthContext.jsx` | Auth state | Current user, login/logout, tokens |

### Important Directories

| Path | What Goes Here | Examples |
|------|----------------|----------|
| `src/features/auth/` | ALL auth code | Login, register, password reset |
| `src/features/student/` | ALL student code | Profile, CV, applications |
| `src/features/opportunities/` | ALL opportunity code | Search, filter, browse |
| `src/components/common/` | Shared UI | Button, Modal, Card, Input |
| `src/hooks/` | Shared custom hooks | useApi, usePagination, useAuth |
| `src/utils/` | Utility functions | validators, formatters, errorHandler |

### Frontend Routing (in App.jsx)

```javascript
// Example routing structure
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from './context/AuthContext';

// Pages
import LoginPage from './features/auth/pages/LoginPage';
import RegisterPage from './features/auth/pages/RegisterPage';
import StudentDashboard from './features/student/pages/StudentDashboard';
import EmployerDashboard from './features/employer/pages/EmployerDashboard';
import AdminDashboard from './features/admin/pages/AdminDashboard';
import OpportunitiesList from './features/opportunities/pages/OpportunitiesList';

function App() {
  const { user } = useContext(AuthContext);
  
  return (
    <BrowserRouter>
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        
        {/* Protected routes - role-based */}
        <Route 
          path="/dashboard" 
          element={
            user?.role === 'student' ? <StudentDashboard /> :
            user?.role === 'employer' ? <EmployerDashboard /> :
            user?.role === 'admin' ? <AdminDashboard /> :
            <Navigate to="/login" />
          } 
        />
        
        <Route path="/opportunities" element={<OpportunitiesList />} />
        
        {/* Default redirect */}
        <Route path="/" element={<Navigate to={user ? "/dashboard" : "/login"} />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
```

---

## Backend Key Files at a Glance

### Core Configuration Files

| File | Purpose | Key Content |
|------|---------|-------------|
| `manage.py` | Django CLI | Run migrations, tests, server |
| `attachlink/settings/base.py` | Django settings | INSTALLED_APPS, DATABASES, MIDDLEWARE |
| `attachlink/urls.py` | Main URL router | Include all app URLs |
| `requirements.txt` | Dependencies | Django, DRF, psycopg2, Pillow, etc |

### Important Directories

| Path | What Goes Here | Examples |
|------|----------------|----------|
| `apps/users/` | Auth system | User model, JWT, permissions |
| `apps/students/` | Student features | StudentProfile, CV upload |
| `apps/employers/` | Employer features | Employer model, Company model |
| `apps/opportunities/` | Opportunity features | Opportunity CRUD, search/filter |
| `apps/applications/` | Application features | Application tracking, status updates |
| `apps/admin_panel/` | Admin features | User management, verification |
| `utils/` | Shared utilities | Validators, permissions, responses |

### Backend API Structure (in attachlink/urls.py)

```python
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Authentication
    path('api/auth/', include('apps.users.urls')),  # /api/auth/register/, /api/auth/login/
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Students
    path('api/students/', include('apps.students.urls')),  # /api/students/
    
    # Employers
    path('api/employers/', include('apps.employers.urls')),  # /api/employers/
    
    # Opportunities
    path('api/opportunities/', include('apps.opportunities.urls')),  # /api/opportunities/
    
    # Applications
    path('api/applications/', include('apps.applications.urls')),  # /api/applications/
    
    # Admin
    path('api/admin/', include('apps.admin_panel.urls')),  # /api/admin/
]
```

### Backend Model Relationships

```
User (Base)
├── StudentProfile (One-to-One)
├── Employer (One-to-One)
└── AdminUser (One-to-One)

Employer
└── Opportunity (One-to-Many)
    └── Application (One-to-Many)

StudentProfile
└── Application (One-to-Many)
```

---

## File Naming Conventions

### Frontend

| Type | Convention | Example |
|------|-----------|---------|
| **Page Component** | PascalCase.jsx | StudentDashboard.jsx |
| **Reusable Component** | PascalCase.jsx | Button.jsx |
| **Custom Hook** | useXxx.js | useAuth.js, useApi.js |
| **Service** | xxxService.js | studentService.js |
| **Utility** | xxxUtils.js or xxx.js | validators.js, formatters.js |
| **Context** | XxxContext.jsx | AuthContext.jsx |
| **Type** | xxx.types.js | user.types.js |
| **Constant** | CONSTANT_NAME (in files) | USER_ROLES, API_ENDPOINTS |

### Backend

| Type | Convention | Example |
|------|-----------|---------|
| **Model** | PascalCase | class StudentProfile |
| **Serializer** | XxxSerializer | StudentProfileSerializer |
| **ViewSet** | XxxViewSet | StudentViewSet |
| **Permission** | IsPascalCase | IsStudent, IsOwner |
| **Validator** | validate_xxx | validate_password, validate_cv_file |
| **Utility Function** | snake_case | send_email, format_date |

---

## Feature Integration Pattern

### Adding a New Feature (Example: "Resume Parser")

#### Frontend Steps:

```
1. Create feature folder:
   src/features/resume-parser/

2. Create subdirectories:
   ├── components/
   │   ├── ResumeUploader.jsx
   │   └── ParsedResults.jsx
   ├── pages/
   │   └── ResumeParserPage.jsx
   ├── services/
   │   └── resumeParserService.js      ← Calls API
   ├── hooks/
   │   └── useResumeParser.js          ← Shared logic
   └── index.js                         ← Exports

3. Create service (resumeParserService.js):
   export async function parseResume(file) {
     return api.post('/api/resume-parser/parse/', 
       { file }, 
       { headers: { 'Content-Type': 'multipart/form-data' } }
     );
   }

4. Add route in App.jsx:
   <Route path="/resume-parser" element={<ResumeParserPage />} />

5. Add navigation link in Header.jsx
```

#### Backend Steps:

```
1. Create Django app:
   python manage.py startapp resume_parser

2. Create models (resume_parser/models.py):
   class ParsedResume(models.Model):
       user = ForeignKey(User, ...)
       original_file = FileField(...)
       parsed_data = JSONField(...)

3. Create serializer (resume_parser/serializers.py):
   class ParsedResumeSerializer(ModelSerializer):
       class Meta:
           model = ParsedResume
           fields = [...]

4. Create view (resume_parser/views.py):
   class ParseResumeView(APIView):
       permission_classes = [IsAuthenticated]
       
       def post(self, request):
           file = request.FILES['file']
           # Parse resume logic
           return Response({...})

5. Add URL (resume_parser/urls.py):
   urlpatterns = [
       path('parse/', ParseResumeView.as_view()),
   ]

6. Include in main urls.py:
   path('api/resume-parser/', include('apps.resume_parser.urls'))

7. Add app to INSTALLED_APPS in settings/base.py:
   INSTALLED_APPS = [
       ...
       'apps.resume_parser',
   ]

8. Create migration:
   python manage.py makemigrations
   python manage.py migrate

9. Create tests (tests/resume_parser/):
   - test_models.py
   - test_views.py
```

---

## Data Flow Examples

### Example 1: Student Login

```
Frontend                          Backend
─────────────────────────────────────────
                           User clicks Login button
                                   │
                                   ↓
                    <LoginPage> renders LoginForm
                                   │
                    User enters email & password
                                   │
                            Form validates locally
                                   │
                           POST /api/auth/login/
                           (JSON: email, password)
                                   ↓
                        ──────────────────────
                        users/views.py:LoginView
                          - Find user by email
                          - Hash password matches?
                          - Generate JWT token
                        ──────────────────────
                                   ↓
                        Response: {
                          "access_token": "...",
                          "user": {
                            "id": 5,
                            "email": "...",
                            "role": "student"
                          }
                        }
                                   ↓
               AuthContext updates state
          localStorage.setItem('access_token', ...)
          Redirect to /dashboard
                                   │
                    <StudentDashboard> renders
                                   │
                                ✅ Success!
```

### Example 2: Student Applies for Opportunity

```
Frontend                          Backend
─────────────────────────────────────────
User on <OpportunityDetailPage>
    │
    └→ Clicks "Apply Now" button
        │
        ↓
    <ApplicationForm> opens
        │
    User fills form (cover letter, availability)
        │
    Click "Submit Application"
        │
        POST /api/applications/
        Header: Authorization: Bearer {token}
        JSON: {
          "opportunity_id": 42,
          "cover_letter": "..."
        }
                              ↓
                   ──────────────────────
                   applications/views.py:ApplicationViewSet.create()
                   
                   1. Verify user is student
                   2. Check if already applied
                   3. Create Application object
                   4. Save to database
                   5. Fire signal → Send email notification
                   ──────────────────────
                              ↓
                   Response: {
                     "id": 999,
                     "status": "pending",
                     "applied_at": "2024-01-15T10:30:00Z"
                   }
                              ↓
        Response received ✓
        
        Show success message
        Redirect to <MyApplications>
               │
               ↓
        Display application in list
               │
            ✅ Success!
```

### Example 3: Employer Verifies Applicant (Admin Rejects)

```
Frontend (Admin Panel)            Backend
─────────────────────────────────────────
Admin on <AdminDashboard>
    │
    └→ Clicks "Verify Employers"
        │
        ↓
    GET /api/admin/unverified-employers/
                              ↓
            ──────────────────────
            admin_panel/views.py:UnverifiedEmployersView.get()
            - Query Employer.objects.filter(verified_at=None)
            - Serialize each employer
            ──────────────────────
                              ↓
        Response: [
          {
            "id": 1,
            "company_name": "Not Real Corp",
            "status": "unverified"
          },
          ...
        ]
                              ↓
        Admin sees list
        │
        Clicks "Reject" on employer
        │
        POST /api/admin/reject-employer/1/
        JSON: {
          "reason": "Fraudulent company"
        }
                              ↓
            ──────────────────────
            admin_panel/views.py:RejectEmployerView.post()
            - Find employer
            - Delete account or mark as banned
            - Send email notification
            ──────────────────────
                              ↓
        Response: {"status": "rejected"}
                              ↓
        Admin UI updated
        Employer receives rejection email
        ✅ Admin action complete!
```

---

## Common File Imports

### Frontend

```javascript
// Components
import Button from 'src/components/common/Button';
import StudentCard from 'src/features/student/components/StudentCard';

// Services & API
import api from 'src/services/api';
import studentService from 'src/features/student/services/studentService';

// Hooks
import useApi from 'src/hooks/useApi';
import useAuth from 'src/features/auth/hooks/useAuth';

// Context
import { AuthContext } from 'src/context/AuthContext';

// Utils
import { validateEmail } from 'src/utils/validators';
import { formatDate } from 'src/utils/formatters';

// Constants
import { USER_ROLES } from 'src/constants/roles';
import { APPLICATION_STATUS } from 'src/constants/status';

// Types
import { User, StudentProfile } from 'src/types/user.types';
```

### Backend

```python
# Models
from apps.users.models import User
from apps.students.models import StudentProfile
from apps.opportunities.models import Opportunity

# Serializers
from apps.students.serializers import StudentProfileSerializer
from apps.opportunities.serializers import OpportunitySerializer

# Views
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

# Permissions
from utils.permissions import IsStudent, IsEmployer, IsAuthenticated
from rest_framework.permissions import IsAuthenticated

# Validators
from utils.validators import validate_email, validate_cv_file

# Django
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
```

---

## Environment Variables

### Frontend (.env.local)

```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_TIMEOUT=10000
REACT_APP_DEBUG=true
```

### Backend (.env)

```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/attachlink_db

# Email
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_FROM=noreply@attachlink.com

# JWT
JWT_SECRET=your-jwt-secret

# Supabase (for production)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

---

## Git Workflow

### Branch Naming Convention

```
feature/[feature-name]        # New feature
  feature/student-cv-upload

bugfix/[bug-description]      # Bug fix
  bugfix/login-token-expiry

hotfix/[issue-description]    # Critical production fix
  hotfix/database-connection-error

docs/[doc-name]               # Documentation
  docs/api-endpoints
```

### Commit Messages

```
feat: Add student CV upload functionality
fix: Resolve JWT token expiry bug
refactor: Reorganize auth service structure
docs: Update API documentation
test: Add tests for opportunity filtering
chore: Update dependencies
```

---

## Quick Command Reference

### Frontend

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Run tests
npm run test

# Format code
npm run format
```

### Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver

# Run tests
pytest

# Collect static files
python manage.py collectstatic
```

### Docker

```bash
# Build images and start services
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f backend
```

---

## File Size Guidelines

### Frontend

- Page components: 300-500 lines (split if larger)
- Feature service: 100-200 lines
- Custom hooks: 50-150 lines
- Utility functions: 20-50 lines per function

### Backend

- Models file: 200-400 lines (split if larger)
- Serializers file: 100-200 lines
- Views file: 150-250 lines
- Tests file: 300+ lines (comprehensive)

---

## Red Flags (Things to Avoid)

❌ Importing from `parent_feature` into `different_feature`
❌ Putting all utilities in one giant file
❌ ComponentSpecificService.js in `common/`
❌ Hardcoding API URLs in components
❌ Storing JWT token in state (use localStorage)
❌ Circular imports between Django apps
❌ Model logic in views (put in models or services)
❌ 1000+ line files

✅ Better Alternatives:

✅ API calls through services
✅ Organized utilities by purpose
✅ Constants in constants/ folder
✅ Single source of truth for API URLs
✅ Persistent storage for tokens
✅ Shared utils/ for common logic
✅ Model methods for business logic
✅ Split files when they get too large

