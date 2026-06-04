# AttachLink - Folder Purpose Reference

## Complete Folder Breakdown with Explanations

---

## Frontend Structure: Detailed Purposes

### `/frontend/src/components/` - Reusable UI Components

**Purpose**: Store components that are used across multiple features. Think of these as your "UI library."

**When to put something here**:
- ✅ Used by 2+ features
- ✅ Generic/not tied to specific feature logic
- ✅ Examples: Button, Modal, Card, Input, Badge

**Structure**:
```
components/
├── common/          # Generic UI components
│   ├── Button.jsx          # Reusable button (used in auth, student, employer)
│   ├── Modal.jsx           # Reusable modal dialog
│   ├── Input.jsx           # Form input with validation
│   ├── Card.jsx            # Container component
│   ├── Badge.jsx           # Status badge (for application status, etc)
│   ├── Alert.jsx           # Alert/notification component
│   └── Pagination.jsx      # Pagination controls
│
└── layout/          # App structure components
    ├── Header.jsx          # Top navigation bar
    ├── Sidebar.jsx         # Left sidebar (if applicable)
    ├── Footer.jsx          # Footer component
    ├── MainLayout.jsx      # Main app layout wrapper
    └── ProtectedRoute.jsx  # Route that checks authentication
```

**Example Usage**:
```javascript
// In any component
import { Button } from 'src/components/common/Button';
import { Modal } from 'src/components/common/Modal';

function MyComponent() {
  return (
    <>
      <Button>Click Me</Button>
      <Modal>Content</Modal>
    </>
  );
}
```

---

### `/frontend/src/features/` - Feature Modules

**Purpose**: Group all code related to a specific feature. Each feature is self-contained and can work independently.

**Features Breakdown**:

#### 1. **auth/** - Authentication Feature
**What lives here**: Login, registration, password reset, email verification

```
auth/
├── components/
│   ├── LoginForm.jsx          # Email + password form
│   ├── RegisterForm.jsx       # Registration form with role selector
│   ├── RoleSelector.jsx       # Choose student/employer/admin
│   ├── PasswordResetForm.jsx  # Reset password link
│   └── EmailVerification.jsx  # Verify email token
│
├── pages/
│   ├── LoginPage.jsx          # Full page for login
│   ├── RegisterPage.jsx       # Full page for registration
│   ├── VerifyEmailPage.jsx    # Email verification page
│   └── PasswordResetPage.jsx  # Password reset page
│
├── hooks/
│   ├── useAuth.js             # Get current user, logout
│   ├── useLogin.js            # Login logic
│   ├── useRegister.js         # Register logic
│   └── usePasswordReset.js    # Reset password logic
│
├── services/
│   └── authService.js         # API calls: register, login, verify, refresh token
│
└── index.js                   # Exports: LoginPage, RegisterPage, etc
```

**Key responsibilities**:
- User registration (with role selection)
- User login (returns JWT token)
- Email verification
- Password reset
- Token refresh

**Who uses this**:
- Everyone (non-authenticated users need this first)

#### 2. **student/** - Student Feature
**What lives here**: Student profile, CV upload, search opportunities, track applications

```
student/
├── components/
│   ├── StudentCard.jsx        # Display student info
│   ├── ProfileForm.jsx        # Edit student profile (university, skills, GPA)
│   ├── CVUploader.jsx         # Upload/manage CV files
│   ├── StudentFilters.jsx     # Filter opportunities (location, role type, etc)
│   └── SkillsInput.jsx        # Add/remove skills
│
├── pages/
│   ├── StudentDashboard.jsx   # Main student dashboard
│   ├── StudentProfile.jsx     # View/edit student profile
│   ├── MyApplications.jsx     # Track applications (status, dates)
│   └── OpportunitySearch.jsx  # Browse and search opportunities
│
├── services/
│   └── studentService.js      # API calls: upload CV, update profile, get applications
│
└── index.js
```

**Key responsibilities**:
- Create/edit student profile
- Upload CV (validation, file management)
- View all opportunities
- Apply for opportunities
- Track application status

**Who uses this**:
- Students only (protected by `IsStudent` permission)

#### 3. **employer/** - Employer Feature
**What lives here**: Company profile, post opportunities, manage applicants

```
employer/
├── components/
│   ├── EmployerCard.jsx       # Display company info
│   ├── CompanyForm.jsx        # Edit company profile
│   ├── ApplicantsList.jsx     # List applicants for an opportunity
│   ├── EmployerFilters.jsx    # Filter applicants
│   └── ApplicationReview.jsx  # Review individual application (accept/reject)
│
├── pages/
│   ├── EmployerDashboard.jsx  # Main employer dashboard (stats, applications)
│   ├── CompanyProfile.jsx     # View/edit company profile
│   ├── MyOpportunities.jsx    # List all their posted opportunities
│   └── ManageApplications.jsx # Manage incoming applications from students
│
├── services/
│   └── employerService.js     # API calls: update company, post opportunity, review apps
│
└── index.js
```

**Key responsibilities**:
- Create/edit company profile
- Post new opportunities
- Edit/delete opportunities
- View applicants for each opportunity
- Accept/reject applications

**Who uses this**:
- Employers only (protected by `IsEmployer` permission)

#### 4. **opportunities/** - Opportunity Listing & Discovery
**What lives here**: Browse, search, filter opportunities (used by students and employers)

```
opportunities/
├── components/
│   ├── OpportunityCard.jsx    # Individual opportunity card (title, salary, deadline)
│   ├── OpportunityDetail.jsx  # Detailed view (description, requirements, company)
│   ├── OpportunityForm.jsx    # Create/edit opportunity form
│   ├── SearchBar.jsx          # Search by title/company
│   ├── FilterPanel.jsx        # Filter (location, salary range, type, deadline)
│   └── SortOptions.jsx        # Sort (newest, deadline, salary)
│
├── pages/
│   ├── OpportunitiesList.jsx  # Main browse page with search & filters
│   ├── OpportunityDetailPage.jsx # Full page for single opportunity
│   └── CreateOpportunity.jsx  # Employer creates new opportunity
│
├── services/
│   └── opportunityService.js  # API calls: list, search, filter, create, update, delete
│
└── index.js
```

**Key responsibilities**:
- List all opportunities (with pagination)
- Search opportunities (by title, company, location)
- Filter opportunities (salary range, deadline, opportunity type)
- View opportunity details
- Create/edit opportunities (for employers)
- Apply for opportunity (redirects to applications/)

**Who uses this**:
- Students (view-only)
- Employers (view-only + create/edit their own)

#### 5. **applications/** - Application Management
**What lives here**: Student apply for opportunities, employers review, track status

```
applications/
├── components/
│   ├── ApplicationCard.jsx    # Individual application card
│   ├── ApplicationForm.jsx    # Apply form (cover letter, availability)
│   ├── ApplicationStatus.jsx  # Status badge (pending, accepted, rejected)
│   ├── ApplicantInfo.jsx      # Display student applicant info (resume)
│   └── StatusTimeline.jsx     # Show application timeline
│
├── pages/
│   ├── ApplicationsPage.jsx   # All applications (for employer - incoming)
│   ├── ApplicationDetail.jsx  # Full application details (for employer to review)
│   ├── StudentApplications.jsx # Student's own applications (track status)
│   └── ApplyPage.jsx          # Student apply for opportunity form
│
├── services/
│   └── applicationService.js  # API calls: apply, get applications, update status
│
└── index.js
```

**Key responsibilities**:
- Student apply for opportunity
- Student view their application tracker
- Employer view applicants for each opportunity
- Employer accept/reject applications
- Track application status (pending → accepted/rejected)

**Who uses this**:
- Students (apply, track)
- Employers (review, accept/reject)

#### 6. **admin/** - Admin Management
**What lives here**: Admin dashboard, user management, fraud detection

```
admin/
├── components/
│   ├── UserManagement.jsx     # List users, toggle active status
│   ├── EmployerVerification.jsx # Verify/reject employer accounts
│   ├── FlaggedContent.jsx     # Review flagged opportunities/applications
│   ├── UserStats.jsx          # User statistics cards
│   ├── ActivityLog.jsx        # System-wide activity log
│   └── ReportsTable.jsx       # Detailed reports table
│
├── pages/
│   ├── AdminDashboard.jsx     # Main admin dashboard (stats, overview)
│   ├── UsersPage.jsx          # Manage all users
│   ├── EmployerVerificationPage.jsx # Verify/approve employers
│   ├── FlaggedContentPage.jsx # Review flagged opportunities
│   └── ReportsPage.jsx        # Detailed analytics & reports
│
├── services/
│   └── adminService.js        # API calls: manage users, verify employers, flag content
│
└── index.js
```

**Key responsibilities**:
- View system statistics (total users, applications, etc)
- Manage users (activate, deactivate, delete)
- Verify employer companies
- Review flagged opportunities (spam, wrong category)
- View activity logs
- Generate reports

**Who uses this**:
- Admins only (protected by `IsAdmin` permission)

---

### `/frontend/src/hooks/` - Shared Custom Hooks

**Purpose**: Reusable React logic that can be used in multiple components.

**Examples**:
```javascript
// useApi.js - Handles loading/error states for API calls
export function useApi(apiFunction) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);
  
  const execute = async () => {
    // implementation
  };
  
  return { loading, error, data, execute };
}

// Usage in any component:
function StudentDashboard() {
  const { loading, data: students } = useApi(studentService.getAll);
  return <div>{students?.map(s => <div>{s.name}</div>)}</div>;
}
```

**Common hooks**:
- `useApi()` - Fetch data, handle loading/errors
- `usePagination()` - Manage pagination state
- `useLocalStorage()` - Sync state with localStorage
- `useDebounce()` - Debounce search input
- `useModal()` - Show/hide modal logic
- `useForm()` - Handle form state and validation
- `useAuth()` - Get current user, logout

---

### `/frontend/src/services/` - Global Services

**Purpose**: Shared API communication logic

```
services/
├── api.js              # Axios instance with interceptors
│                       # - Auto-injects JWT token
│                       # - Handles 401 errors (refresh token)
│                       # - Formats errors consistently
│
└── constants.js        # API endpoint URLs
                        # - BASE_URL = http://localhost:8000
                        # - ENDPOINTS = { auth: {...}, students: {...} }
```

**Example api.js**:
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
});

// Interceptor: Auto-add JWT token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor: Handle 401 errors
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Refresh token or redirect to login
    }
    return Promise.reject(error);
  }
);

export default api;
```

---

### `/frontend/src/utils/` - Utility Functions

**Purpose**: Reusable functions that aren't components or services

```
utils/
├── validators.js       # validate email, password strength, CV file type
├── formatters.js       # format dates, numbers, currencies
├── localStorage.js     # localStorage helpers
├── errorHandler.js     # Parse and display API errors
├── constants.js        # React Query settings, debug flags
└── helpers.js          # General helper functions
```

**Examples**:
```javascript
// validators.js
export function validateEmail(email) {
  return /\S+@\S+\.\S+/.test(email);
}

export function validatePassword(pwd) {
  return pwd.length >= 8 && /[A-Z]/.test(pwd); // At least 8 chars + uppercase
}

export function validateCVFile(file) {
  const validTypes = ['application/pdf', 'application/msword'];
  const maxSize = 5 * 1024 * 1024; // 5MB
  return validTypes.includes(file.type) && file.size <= maxSize;
}

// Usage in form:
if (!validateEmail(form.email)) {
  setError('Invalid email');
}
```

---

### `/frontend/src/context/` - React Context

**Purpose**: Global state accessible to any component without prop drilling

```
context/
├── AuthContext.jsx     # Current user, isAuthenticated, login/logout functions
├── ThemeContext.jsx    # Dark/light mode
└── NotificationContext.jsx # Show toast notifications
```

**Example AuthContext.jsx**:
```javascript
import React, { createContext, useState } from 'react';

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null); // { id, email, role }
  const [isLoading, setIsLoading] = useState(false);
  
  const login = async (email, password) => {
    const data = await authService.login(email, password);
    setUser(data.user);
    localStorage.setItem('access_token', data.access_token);
  };
  
  const logout = () => {
    setUser(null);
    localStorage.removeItem('access_token');
  };
  
  return (
    <AuthContext.Provider value={{ user, login, logout, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
}
```

**Usage**:
```javascript
function MyComponent() {
  const { user, logout } = useContext(AuthContext);
  return <div>Welcome {user.email} <button onClick={logout}>Logout</button></div>;
}
```

---

### `/frontend/src/types/` - Type Definitions

**Purpose**: Document data structures using JSDoc or TypeScript

```
types/
├── user.types.js           # User, StudentProfile, Employer types
├── opportunity.types.js    # Opportunity type
└── application.types.js    # Application type
```

**Example user.types.js**:
```javascript
/**
 * @typedef {Object} User
 * @property {number} id
 * @property {string} email
 * @property {string} role - 'student' | 'employer' | 'admin'
 * @property {string} createdAt
 */

/**
 * @typedef {Object} StudentProfile
 * @property {number} id
 * @property {number} userId
 * @property {string} university
 * @property {number} gpa
 * @property {string[]} skills
 * @property {string} cvFileUrl
 */

export {};
```

---

### `/frontend/src/constants/` - Application Constants

**Purpose**: Store app-wide constants (roles, statuses, messages)

```
constants/
├── roles.js            # USER_ROLES = { STUDENT: 'student', EMPLOYER: 'employer' }
├── status.js           # APPLICATION_STATUS = { PENDING: 'pending', ACCEPTED: 'accepted' }
└── messages.js         # UI messages (success, error, validation messages)
```

**Example**:
```javascript
// roles.js
export const USER_ROLES = {
  STUDENT: 'student',
  EMPLOYER: 'employer',
  ADMIN: 'admin',
};

// status.js
export const APPLICATION_STATUS = {
  PENDING: 'pending',
  ACCEPTED: 'accepted',
  REJECTED: 'rejected',
};

export const OPPORTUNITY_STATUS = {
  OPEN: 'open',
  CLOSED: 'closed',
  EXPIRED: 'expired',
};

// Usage:
if (user.role === USER_ROLES.STUDENT) {
  // show student dashboard
}
```

---

### `/frontend/public/` - Static Assets

**Purpose**: Files that don't need processing (images, favicon, etc)

```
public/
├── index.html          # HTML entry point
├── favicon.ico         # Browser tab icon
├── logo.svg            # App logo
└── images/
    ├── hero.jpg        # Hero section image
    ├── placeholder.jpg # Placeholder images
    └── ...
```

---

## Backend Structure: Detailed Purposes

### `/backend/attachlink/` - Project Configuration

**Purpose**: Django project-level settings and routing

```
attachlink/
├── settings/
│   ├── base.py         # Base settings (INSTALLED_APPS, DATABASES, MIDDLEWARE, CORS)
│   ├── local.py        # Local development overrides (DEBUG=True, EMAIL_BACKEND=console)
│   ├── production.py   # Production overrides (DEBUG=False, SECURE_SSL_REDIRECT=True)
│   └── __init__.py
│
├── urls.py             # Main URL router that includes all app URLs
│                       # - path('api/auth/', include('apps.users.urls'))
│                       # - path('api/students/', include('apps.students.urls'))
│                       # - etc
│
├── asgi.py             # ASGI config (for production: Daphne, Uvicorn)
├── wsgi.py             # WSGI config (for production: Gunicorn)
└── __init__.py
```

**Key settings file content**:
```python
# settings/base.py
INSTALLED_APPS = [
    # Django built-in
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    
    # Third-party
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    
    # Our apps
    'apps.users',
    'apps.students',
    'apps.employers',
    'apps.opportunities',
    'apps.applications',
    'apps.admin_panel',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'attachlink_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

### `/backend/apps/` - Django Applications

**Purpose**: Each app is a self-contained module with its own models, views, serializers

#### **apps/users/** - User Management & Authentication

**Files**:
- `models.py` → User model, Role model
- `views.py` → Register, Login, Refresh token endpoints
- `serializers.py` → UserSerializer, RegisterSerializer, validation
- `authentication.py` → JWT token verification
- `permissions.py` → Permission classes (IsAuthenticated, IsStudent, IsEmployer, IsAdmin)
- `urls.py` → Auth URLs

**Key responsibilities**:
- User registration with role selection
- User login (JWT token generation)
- Token refresh
- User profile retrieval
- Role-based access control

**Models**:
```python
class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(
        max_length=20,
        choices=[
            ('student', 'Student'),
            ('employer', 'Employer'),
            ('admin', 'Admin'),
        ]
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

---

#### **apps/students/** - Student Profiles

**Files**:
- `models.py` → StudentProfile model
- `views.py` → Get/update student profile, upload CV
- `serializers.py` → StudentProfileSerializer
- `urls.py` → Student URLs

**Key responsibilities**:
- Student profile CRUD (create, read, update)
- CV file upload and validation
- Skills management
- Student search and listing

**Models**:
```python
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university = models.CharField(max_length=255)
    gpa = models.DecimalField(max_digits=3, decimal_places=2)  # e.g., 3.85
    cv_file = models.FileField(upload_to='cvs/')
    skills = models.TextField()  # JSON or comma-separated
    created_at = models.DateTimeField(auto_now_add=True)
```

---

#### **apps/employers/** - Employer Profiles

**Files**:
- `models.py` → Employer model, Company model
- `views.py` → Get/update employer profile, company info
- `serializers.py` → EmployerSerializer, CompanySerializer
- `urls.py` → Employer URLs

**Key responsibilities**:
- Employer profile CRUD
- Company info management (logo, description, verified status)
- Employer listing

**Models**:
```python
class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    company_logo = models.ImageField(upload_to='company_logos/')
    industry = models.CharField(max_length=100)
    description = models.TextField()
    verified_at = models.DateTimeField(null=True)  # When admin verified
    created_at = models.DateTimeField(auto_now_add=True)
```

---

#### **apps/opportunities/** - Opportunity Management

**Files**:
- `models.py` → Opportunity model
- `views.py` → List, create, update, delete opportunities
- `serializers.py` → OpportunitySerializer
- `filters.py` → Filtering, searching, sorting logic
- `urls.py` → Opportunity URLs

**Key responsibilities**:
- Create/edit/delete opportunities (employers only)
- List opportunities (with search, filters, sorting)
- Opportunity details retrieval

**Models**:
```python
class Opportunity(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)  # e.g., "Python Developer Internship"
    description = models.TextField()
    requirements = models.TextField()  # JSON or text
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    location = models.CharField(max_length=255)
    deadline = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('open', 'Open'),
            ('closed', 'Closed'),
            ('filled', 'Filled'),
        ],
        default='open'
    )
    created_at = models.DateTimeField(auto_now_add=True)
```

---

#### **apps/applications/** - Application Tracking

**Files**:
- `models.py` → Application model
- `views.py` → Apply for opportunity, list applications, update status
- `serializers.py` → ApplicationSerializer
- `signals.py` → Send notifications when status changes
- `urls.py` → Application URLs

**Key responsibilities**:
- Student apply for opportunity
- List applications (for student or employer)
- Update application status (accept/reject)
- Send notifications

**Models**:
```python
class Application(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    cover_letter = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True)
```

---

#### **apps/admin_panel/** - Admin Management

**Files**:
- `models.py` → FlaggedContent, AdminAction models
- `views.py` → User management, employer verification, reports
- `serializers.py` → Serializers for admin endpoints
- `urls.py` → Admin URLs

**Key responsibilities**:
- User management (list, activate, deactivate, delete)
- Employer verification
- Flag/remove fraudulent opportunities
- System analytics and reports

**Models**:
```python
class FlaggedContent(models.Model):
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, null=True)
    reason = models.CharField(max_length=255)  # 'spam', 'inappropriate', etc
    flagged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

---

### `/backend/utils/` - Shared Utilities

**Purpose**: Reusable functions for validation, permissions, responses, etc

```
utils/
├── validators.py       # Validate email format, password strength, CV file
├── decorators.py       # @require_role, @ensure_owner, etc
├── exceptions.py       # Custom exceptions (InvalidRoleError, etc)
├── pagination.py       # Custom pagination for DRF
├── response.py         # Standardized API response format
├── file_handlers.py    # File upload, validation, storage
├── email_service.py    # Send emails (verification, notifications)
├── notifications.py    # In-app notifications
├── constants.py        # App constants (roles, statuses, etc)
└── __init__.py
```

**Example validators.py**:
```python
def validate_email(email):
    """Ensure email is valid format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password_strength(password):
    """Ensure password meets requirements"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not any(c.isupper() for c in password):
        return False, "Password must contain uppercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain digit"
    return True, "Valid password"

def validate_cv_file(file):
    """Ensure CV file is PDF or DOCX, max 5MB"""
    valid_types = ['application/pdf', 'application/msword']
    max_size = 5 * 1024 * 1024  # 5MB
    
    if file.content_type not in valid_types:
        return False, "CV must be PDF or DOC"
    if file.size > max_size:
        return False, "CV must be under 5MB"
    return True, "Valid CV"
```

**Example permissions.py**:
```python
from rest_framework import permissions

class IsStudent(permissions.BasePermission):
    """Allow only students"""
    def has_permission(self, request, view):
        return request.user and request.user.role == 'student'

class IsEmployer(permissions.BasePermission):
    """Allow only employers"""
    def has_permission(self, request, view):
        return request.user and request.user.role == 'employer'

class IsAdmin(permissions.BasePermission):
    """Allow only admins"""
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'

class IsOwner(permissions.BasePermission):
    """Allow only if user owns the resource"""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
```

---

### `/backend/tests/` - Test Suite

**Purpose**: Unit and integration tests for all functionality

```
tests/
├── users/
│   ├── test_models.py         # Test User model fields, validation
│   ├── test_views.py          # Test auth endpoints (register, login)
│   ├── test_serializers.py    # Test UserSerializer validation
│   └── __init__.py
│
├── students/
│   ├── test_models.py         # Test StudentProfile model
│   ├── test_views.py          # Test student endpoints
│   └── ...
│
├── employers/
│   └── ...
│
├── opportunities/
│   └── ...
│
├── applications/
│   └── ...
│
├── conftest.py                # Pytest configuration, shared fixtures
│   # Example fixtures:
│   # - @pytest.fixture - get_test_user()
│   # - @pytest.fixture - get_test_student()  
│   # - @pytest.fixture - client (authenticated API client)
│
└── __init__.py
```

**Example test**:
```python
# tests/users/test_views.py
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestAuthViews:
    def test_user_registration(self):
        client = APIClient()
        response = client.post('/api/auth/register/', {
            'email': 'john@example.com',
            'password': 'SecurePass123',
            'role': 'student',
        })
        
        assert response.status_code == 201
        assert response.data['user']['email'] == 'john@example.com'
        assert response.data['access_token']
```

---

### `/backend/media/` - User Uploads

**Purpose**: Store user-uploaded files

```
media/
├── cvs/                   # Student CV files
│   └── cv_12345.pdf
│
├── company_logos/         # Company logos
│   └── company_678.png
│
└── profile_pictures/      # User profile pictures
    └── user_123.jpg
```

---

### `/backend/static/` - Static Files

**Purpose**: Compiled CSS, JS, and other static assets (for production)

(Typically populated by `python manage.py collectstatic`)

---

### `/backend/logs/` - Application Logs

**Purpose**: Store application error and access logs

```
logs/
├── django.log     # Django application logs
├── celery.log     # Background task logs
└── access.log     # HTTP request logs
```

---

## Documentation: Detailed Purposes

### `/docs/api/` - API Endpoint Documentation

**Files**:
- `authentication.md` → JWT flow, register/login endpoints
- `students.md` → Student endpoints with request/response examples
- `employers.md` → Employer endpoints
- `opportunities.md` → Opportunity CRUD endpoints
- `applications.md` → Application endpoints
- `admin.md` → Admin management endpoints
- `error_codes.md` → Error response codes and meanings

**Example documentation**:
```markdown
# Student Endpoints

## Get Student Profile
GET /api/students/12/

**Headers**: Authorization: Bearer {token}

**Response (200)**:
{
  "id": 12,
  "user": {"id": 5, "email": "john@uni.edu"},
  "university": "MIT",
  "gpa": 3.85,
  "skills": ["Python", "React"],
  "cv_file": "https://api.attachlink.com/media/cvs/cv_123.pdf"
}

## Upload CV
POST /api/students/12/upload-cv/

**Headers**: Authorization: Bearer {token}
**Body**: multipart/form-data
  - file: (binary PDF/DOC file)

**Response (200)**:
{
  "cv_file": "https://api.attachlink.com/media/cvs/cv_456.pdf"
}
```

---

### `/docs/architecture/` - System Design Documentation

**Files**:
- `ARCHITECTURE.md` → High-level architecture overview (THIS IS DONE!)
- `database_schema.md` → ER diagram and table relationships
- `auth_flow.md` → How JWT authentication works
- `deployment.md` → Docker, production server setup

---

### `/docs/guides/` - Developer Guides

**Files**:
- `SETUP.md` → How to set up local development environment
- `CONTRIBUTING.md` → How to contribute (branching, PR format, review process)
- `TESTING.md` → How to run tests (frontend + backend)
- `TROUBLESHOOTING.md` → Common errors and solutions

---

## Top-Level Configuration Files

| File | Purpose |
|------|---------|
| `.gitignore` | Files to ignore in version control (node_modules, .env, __pycache__, venv) |
| `README.md` | Project overview, quick start, tech stack |
| `docker-compose.yml` | Orchestrate frontend, backend, database containers |
| `FOLDER_STRUCTURE.md` | Detailed explanation (MAIN DOCUMENT) |
| `PROJECT_TREE.md` | Visual tree of entire project |

---

## Summary: When to Put Code Where?

```
Need a reusable UI component?
  → src/components/common/ (if used by 2+ features)
  → src/features/[feature]/components/ (if specific to one feature)

Need to call the API?
  → src/services/api.js (set up request/response)
  → src/features/[feature]/services/ (write the actual API call)

Need state management?
  → src/context/ (if global like auth)
  → useState in component (if local)
  → Custom hook in src/hooks/ (if reused logic)

Need a utility function?
  → src/utils/ (shared across app)
  → Feature folder (if specific to one feature)

Need a Django model?
  → apps/[app]/models.py

Need an API endpoint?
  → apps/[app]/views.py
  → Create ViewSet that inherits from ModelViewSet

Need business logic?
  → utils/ (if shared across apps)
  → apps/[app]/models.py (if app-specific)
```

---

This complete folder structure is production-ready and scales with your team!

