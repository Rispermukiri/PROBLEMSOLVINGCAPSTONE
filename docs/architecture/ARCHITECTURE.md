# AttachLink - Architecture & Design Rationale

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER'S BROWSER                          │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │        FRONTEND (React + Vite + Tailwind CSS)            │  │
│  │                                                          │  │
│  │  ┌─────────────────────────────────────────────────┐   │  │
│  │  │  Pages (Auth, Dashboard, Opportunities, etc)   │   │  │
│  │  └─────────────────────────────────────────────────┘   │  │
│  │                         ↕                               │  │
│  │  ┌─────────────────────────────────────────────────┐   │  │
│  │  │  Components (Shared, Feature-specific)          │   │  │
│  │  └─────────────────────────────────────────────────┘   │  │
│  │                         ↕                               │  │
│  │  ┌─────────────────────────────────────────────────┐   │  │
│  │  │  Context + Hooks (State, Auth, API calls)      │   │  │
│  │  └─────────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                    HTTPS REST API
                    (JSON requests/responses)
                           │
         ┌─────────────────┴─────────────────┐
         │                                   │
         ↓                                   ↓
┌──────────────────────────┐    ┌──────────────────────────┐
│  API SERVER              │    │  DATABASE                │
│  (Django + DRF)          │    │  (Supabase PostgreSQL)   │
│                          │    │                          │
│  ┌────────────────────┐  │    │  ┌──────────────────┐   │
│  │  Authentication    │  │    │  │  Users Table     │   │
│  │  (JWT Tokens)      │  │    │  │  StudentProfile  │   │
│  └────────────────────┘  │    │  │  Employer        │   │
│           ↕              │    │  │  Opportunities   │   │
│  ┌────────────────────┐  │    │  │  Applications    │   │
│  │  Business Logic    │  │    │  │  (More tables)   │   │
│  │  (Validators,      │  │    │  └──────────────────┘   │
│  │   Permissions,     │  │    │                          │
│  │   Services)        │  │    └──────────────────────────┘
│  └────────────────────┘  │
│           ↕              │
│  ┌────────────────────┐  │
│  │  Django Apps       │  │
│  │  (users,           │  │
│  │   students,        │  │
│  │   employers,       │  │
│  │   opportunities,   │  │
│  │   applications,    │  │
│  │   admin_panel)     │  │
│  └────────────────────┘  │
└──────────────────────────┘
```

---

## Frontend Architecture Explained

### Why Feature-Based Organization?

**Traditional Approach (Bad for Scaling):**
```
src/
  components/     # ALL components mixed together
  pages/          # ALL pages mixed together
  services/       # ALL services mixed together
  hooks/          # ALL hooks mixed together
```

**Problem**: As the app grows, finding related code becomes difficult. Updating a feature means jumping between folders.

**Feature-Based Approach (Good for Scaling):**
```
src/features/
  auth/           # All auth code lives here
  student/        # All student code lives here
  opportunities/  # All opp code lives here
```

**Benefits**:
- ✅ Self-contained features (can work independently)
- ✅ Easy to delete/update/scale features
- ✅ Team can own features (Feature A team, Feature B team)
- ✅ Reduced conflicts with Git when multiple teams work in parallel
- ✅ Reusable code (common/ components, utils/) stays separate

### Frontend Folder Structure Breakdown

#### `src/features/*/`
Each feature folder contains:
- **components/** → UI components specific to this feature
- **pages/** → Full-page views for this feature
- **services/** → API calls specific to this feature
- **hooks/** → Custom logic specific to this feature
- **index.js** → Exports all public APIs (for easy imports)

Example: Adding a new "Resume Parser" feature:
```
src/features/resume-parser/
├── components/
│   ├── ResumeUploader.jsx
│   └── ParsedResults.jsx
├── pages/
│   └── ResumeParserPage.jsx
├── services/
│   └── resumeParserService.js
├── hooks/
│   └── useResumeParser.js
└── index.js
```

#### `src/components/common/`
Shared UI components used everywhere:
- `Button.jsx` → Generic button (used in 100+ places)
- `Modal.jsx` → Reusable modal dialog
- `Input.jsx` → Text input with validation
- `Card.jsx` → Container component
- `Badge.jsx` → Status badges

#### `src/services/api.js`
**Central Axios instance with interceptors**:
```javascript
// Automatically:
// - Injects JWT token in every request
// - Handles token refresh
// - Catches & rescues 401 errors
// - Formats error responses
```

#### `src/context/`
Global state (React Context API):
- `AuthContext` → Current user, login state
- `ThemeContext` → Dark/light mode
- `NotificationContext` → Toast notifications

**Why not Redux/Zustand?** For a small-medium app, Context + useState is simpler and sufficient.

#### `src/hooks/`
Shared custom hooks:
- `useApi()` → Wraps API calls with loading/error/data states
- `usePagination()` → Pagination logic
- `useLocalStorage()` → Persistent state
- `useDebounce()` → Debounce search input

#### `src/types/`
Type definitions (if using TypeScript) or JSDoc comments:
```javascript
/**
 * @typedef {Object} User
 * @property {number} id
 * @property {string} email
 * @property {string} role - 'student' | 'employer' | 'admin'
 */
```

### Frontend Data Flow Example

```
User clicks "Search Opportunities" button
  ↓
OpportunitiesList component renders SearchBar
  ↓
User types "Python" & hits Enter
  ↓
SearchBar calls handleSearch() → passes to OpportunitiesList
  ↓
OpportunitiesList calls opportunityService.search("Python")
  ↓
opportunityService calls api.get('/api/opportunities/?search=Python')
  ↓
api.js interceptor adds JWT token to request
  ↓
Request sent to backend
  ↓
Backend returns list of opportunities
  ↓
OpportunitiesList updates state with results
  ↓
Components re-render with new opportunities
  ↓
User sees results
```

---

## Backend Architecture Explained

### Django App-Based Structure

Django's philosophy: "Batteries included" with sensible defaults.

**Each app is independent**:
```
apps/users/
  models.py         # Database schema for this app
  views.py          # API endpoints
  serializers.py    # Validation & JSON conversion
  urls.py           # URL routing for this app
```

**These apps don't know about each other** (loose coupling):
- `students` app doesn't import from `employers` app
- `opportunities` app only imports from `users` for permissions
- Communication happens through the database

### Backend Models Relationships

```
┌─────────────┐
│ User        │  (Base user - inherited by everyone)
│ id          │
│ email       │
│ password    │
│ role        │  ← 'student' | 'employer' | 'admin'
│ created_at  │
└─────────────┘
      ↑
      │ (One-to-One)
      ├──→ StudentProfile (if role='student')
      ├──→ Employer (if role='employer')
      └──→ AdminUser (if role='admin')

StudentProfile
├── user_id (FK) → User
├── cv_file
├── university
├── gpa
└── skills

Employer
├── user_id (FK) → User
├── company_name
├── company_logo
├── verified_at
└── industry

Opportunity
├── employer_id (FK) → Employer
├── title
├── description
├── requirements
├── deadline
└── status ('open' | 'closed' | 'filled')

Application
├── student_id (FK) → StudentProfile
├── opportunity_id (FK) → Opportunity
├── status ('pending' | 'accepted' | 'rejected')
├── applied_at
└── reviewed_at
```

### API Endpoint Structure

Each Django app has its own URL patterns:

**users/urls.py**:
```python
POST /api/auth/register/          # Create new user
POST /api/auth/login/             # Generate JWT token
POST /api/auth/refresh/           # Refresh expired token
GET  /api/users/{id}/             # Get user profile
```

**students/urls.py**:
```python
GET  /api/students/                       # List all students
POST /api/students/                       # Create new student profile
GET  /api/students/{id}/                  # Get specific student
PUT  /api/students/{id}/                  # Update student profile
POST /api/students/{id}/upload-cv/        # Upload CV
```

**opportunities/urls.py**:
```python
GET  /api/opportunities/                  # List with filters
POST /api/opportunities/                  # Create new opp
GET  /api/opportunities/{id}/             # Get details
PUT  /api/opportunities/{id}/             # Update
DELETE /api/opportunities/{id}/           # Delete
```

### Backend Request Flow

```
Frontend sends: POST /api/students/1/upload-cv/
  ↓
Django router finds URL in students/urls.py
  ↓
Calls StudentViewSet.upload_cv() method
  ↓
Permissions checked:
  - @permission_classes([IsAuthenticated, IsStudent])
  - Is user logged in? Yes ✓
  - Is user a student? Yes ✓
  ↓
View processes file upload
  - Calls utils/file_handlers.py:validate_cv()
  - Calls utils/validators.py:validate_file_size()
  ↓
If valid → Save to media/cvs/
  ↓
Update database: StudentProfile.cv_file = new_file_path
  ↓
Create response: {"status": "success", "file_url": "..."}
  ↓
Frontend receives response → Shows success message
```

### Why Separate Utilities?

**Avoid repetition**:
```python
# utils/validators.py (shared)
def validate_email(email):
    # Used by: User registration, email change, employer signup
    
def validate_cv_file(file):
    # Used by: StudentProfile upload, bulk imports
```

**Avoid circular imports**:
If `students/views.py` tried to import directly from `employers/`, it could cause circular import issues. Using utils/ prevents this.

**Centralize business logic**:
```python
# utils/permissions.py
class IsStudent(permissions.BasePermission):
    # Used by: 10+ viewsets that need student permission
```

---

## Authentication Flow (JWT)

### User Registration

```
1. Frontend: POST /api/auth/register/
   {
     "email": "john@uni.edu",
     "password": "secure123",
     "role": "student"   ← Important!
   }

2. Backend: users/views.py:RegisterView
   - Validate email format
   - Check email not already registered
   - Hash password (bcrypt)
   - Create User object with role
   - Return: {"access_token": "...", "refresh_token": "..."}

3. Frontend stores: localStorage.setItem('access_token', token)
   And redirects to role-specific dashboard
```

### User Login

```
1. Frontend: POST /api/auth/login/
   {
     "email": "john@uni.edu",
     "password": "secure123"
   }

2. Backend: users/views.py:LoginView
   - Find user by email
   - Check password matches (bcrypt compare)
   - Generate JWT token: {user_id, email, role, exp}
   - Return: {"access_token": "...", "refresh_token": "..."}

3. Frontend stores token → uses in all API calls
```

### Protected API Requests

```
Frontend needs to GET /api/students/1/

1. Frontend includes token in header:
   Authorization: Bearer eyJhbGc...

2. Backend middleware intercepts request:
   users/authentication.py:JWTAuthentication
   - Decode JWT token
   - Verify signature
   - Check expiration
   - Add user object to request.user

3. View checks permissions:
   @permission_classes([IsAuthenticated, IsStudent])
   - Is request.user set? Yes ✓
   - Is request.user.role == 'student'? Yes ✓
   - Proceed ✓

4. View returns data
```

---

## Why This Architecture?

### ✅ Scalability
- **Add new role?** Create `apps/freelancer/` without touching other apps
- **Add new feature?** Create `src/features/newfeature/` without touching other features
- **Large team?** Team A works on `employer/`, Team B works on `opportunities/`

### ✅ Testability
- **Unit tests**: Test each function in isolation
- **Integration tests**: Test with real database (in tests/)
- **Mock tests**: Mock API calls in frontend tests

### ✅ Reusability
- `common/` components used everywhere
- `utils/` functions shared across apps
- `services/api.js` - single source of truth for API

### ✅ Maintainability
- Code organized by feature/responsibility
- Easy to find code (search `opportunities/` for all opp code)
- Clear data flow (API → Service → Component)

### ✅ Performance
- **Frontend**: Code splitting by route, lazy loading components
- **Backend**: Query optimization, indexes in database, caching
- **Database**: Supabase PostgreSQL (managed, optimized)

---

## Database Technology Choices

### Why PostgreSQL (via Supabase)?

| Feature | PostgreSQL | MySQL | MongoDB |
|---------|-----------|-------|---------|
| **Relationships** | Excellent (FOREIGN KEYS) | Good | Poor (No joins) |
| **Complex Queries** | Excellent (JOIN, GROUP BY) | Good | Limited |
| **ACID Compliance** | Yes (transaction integrity) | Yes | Weak |
| **Auth Requirement** | For role-based access control | | |
| **Our Use Case** | Perfect fit ✅ | Good | Poor |

**Supabase == PostgreSQL + Auth + Realtime + Storage**
- PostgreSQL database
- Built-in authentication
- Real-time subscriptions (for live updates)
- File storage (for CVs, logos)

---

## Frontend Framework Choices

### Why React (not Vue/Angular)?

| Aspect | React | Vue | Angular |
|--------|-------|-----|---------|
| **Learning Curve** | Medium | Easy | Hard |
| **Job Market** | Huge (more jobs) | Growing | Declining |
| **Ecosystem** | Massive (libraries for everything) | Good | Complete (but rigid) |
| **Bundle Size** | Medium | Small | Large |
| **Our Use Case** | Perfect fit ✅ | Good | Overkill |

### Why Vite (not Create React App)?

- **CRA**: 1-2 min build time → Slow during development
- **Vite**: Instant HMR (hot reload) → Fast development experience
- **Bundle size**: Both similar after optimization
- **Modern standard**: Vite is industry standard now (2024+)

### Why Tailwind (not Bootstrap/CSS Modules)?

- **Utility-first**: Write CSS directly in JSX - faster
- **No CSS conflicts**: No naming collisions
- **Smaller bundle**: Only used classes included
- **Consistency**: Design system built-in
- **Mobile-first**: Responsive by default

---

## Deployment Strategy

### Development Environment
```
Frontend: localhost:5173 (Vite dev server)
Backend: localhost:8000 (Django dev server)
Database: Local PostgreSQL or Supabase dev branch
```

### Production Environment
```
Frontend: Vercel/Netlify (auto-deploy on git push)
Backend: Railway/Heroku/AWS EC2 (auto-deploy on git push)
Database: Supabase production (managed, automatic backups)
Storage: Supabase storage for CVs/logos
```

### Docker for Consistency
```
docker-compose up

- Spins up Frontend container
- Spins up Backend container
- Spins up PostgreSQL container (local dev)
- All services communicate via container network
```

---

## Key Technology Stack Summary

| Layer | Technology | Why |
|-------|-----------|-----|
| **Frontend** | React 18 | Industry standard, large ecosystem |
| **Frontend Build** | Vite | Fast, modern, ESM-first |
| **Styling** | Tailwind CSS | Utility-first, rapid development |
| **Routing** | React Router v6 | Standard for React SPAs |
| **HTTP Client** | Axios | Better than fetch, interceptors |
| **State** | Context API + useState | Sufficient for this app size |
| **Backend** | Django 4.2 | Python, batteries included |
| **Backend API** | Django REST Framework | Best Django REST library |
| **Database** | Supabase PostgreSQL | Managed, integrated auth |
| **Authentication** | JWT (access + refresh tokens) | Stateless, scalable |
| **Validation** | Django Serializers + Celery | Built-in, powerful |
| **Testing** | Pytest (Backend), Vitest (Frontend) | Industry standard |
| **DevOps** | Docker + GitHub Actions | Containerized, CI/CD |

---

## Architecture Principles

### 1. **Separation of Concerns**
- Frontend doesn't know business logic
- Backend doesn't know UI
- Database doesn't know API format

### 2. **DRY (Don't Repeat Yourself)**
- Common utilities in `utils/`
- Shared components in `common/`
- Reusable functions everywhere

### 3. **YAGNI (You Aren't Gonna Need It)**
- Don't add features "just in case"
- SOLID principles applied
- Minimal boilerplate

### 4. **Convention over Configuration**
- Django conventions followed
- React patterns followed
- Predictable structure

---

## Next Steps

1. ✅ **Folder Structure Created** (THIS IS DONE!)
2. **Initialize Frontend**: `npm create vite@latest -- --template react`
3. **Initialize Backend**: `django-admin startproject attachlink .`
4. **Set up Database**: Configure Supabase PostgreSQL
5. **Create Core Models**: User, StudentProfile, Employer
6. **Build Authentication**: Registration, Login, JWT tokens
7. **Build Features**: One at a time (Student → Opportunities → Applications)

