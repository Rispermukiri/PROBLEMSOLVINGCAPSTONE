# AttachLink - Django Models Implementation Summary

## ✅ Models Created

All Django models for AttachLink have been designed and implemented with production-quality code. Here's what was created:

---

## 1. **User Model** (`apps/users/models.py`)

**Purpose**: Base authentication model for all users

**Key Features**:
- Role-based system (student, employer, admin)
- Email verification workflow
- Account activation/deactivation
- Last login tracking
- Indexes for performance

**Key Methods**:
```python
user.verify_email()           # Mark email as verified
user.deactivate()             # Deactivate account
user.activate()               # Reactivate account
user.update_last_login()      # Track login time
user.is_student / .is_employer / .is_admin  # Role checks
```

**Indexes**: email, role, is_active (for fast queries)

---

## 2. **AdminUser Model** (`apps/users/models.py`)

**Purpose**: Extended admin profile with permission levels

**Permission Levels**:
- `moderator` - Can moderate content
- `reviewer` - Can verify employers  
- `super_admin` - Full access

**Key Methods**:
```python
admin.can_moderate()          # Check moderation permissions
admin.can_verify_employer()   # Check verification permissions
admin.can_manage_users()      # Check user management permissions
```

---

## 3. **StudentProfile Model** (`apps/students/models.py`)

**Purpose**: Student-specific profile data

**Key Fields**:
| Field | Type | Purpose |
|-------|------|---------|
| `user_id` | OneToOne | Link to User |
| `university` | CharField | School name |
| `gpa` | DecimalField(3,2) | Grade (0.00-4.00) |
| `skills` | JSONField | ["Python", "React", "SQL"] |
| `cv_file` | FileField | PDF/DOCX CV |
| `phone` | CharField | Contact number |
| `bio` | TextField | About student |
| `profile_complete` | BooleanField | 100% complete? |

**Key Methods**:
```python
student.add_skill('Python')
student.remove_skill('Java')
student.has_skill('React')
student.update_cv(file)
student.can_apply              # Can apply for opportunities?
student.get_profile_completeness_percentage()
```

**Validation**:
- GPA must be 0.00-4.00
- At least 1 skill required
- CV file must be PDF/DOCX, max 5MB
- Email must be verified before applying

---

## 4. **Employer Model** (`apps/employers/models.py`)

**Purpose**: Employer company profile

**Key Fields**:
| Field | Type | Purpose |
|-------|------|---------|
| `user_id` | OneToOne | Link to User |
| `company_name` | CharField | Company name |
| `company_logo` | ImageField | Logo image |
| `industry` | CharField | Business sector |
| `website` | URLField | Company website |
| `is_verified` | BooleanField | Admin verified? |
| `verified_by` | ForeignKey(User) | Admin who verified |
| `is_banned` | BooleanField | Policy violation? |

**Key Methods**:
```python
employer.verify(admin_user, notes='')      # Admin verifies
employer.reject_verification(admin_user, reason)  # Reject
employer.can_post_opportunities()          # Can post?
employer.get_pending_applications_count()
employer.get_active_opportunities_count()
```

**Business Rules**:
- Must be verified by admin before posting
- Can be banned for policy violations
- Statistics tracked (postings, applications)

---

## 5. **Opportunity Model** (`apps/opportunities/models.py`)

**Purpose**: Internship/attachment internship postings

**Key Fields**:
| Field | Type | Purpose |
|-------|------|---------|
| `employer_id` | ForeignKey | Who posted |
| `title` | CharField | Job title |
| `description` | TextField | Full description |
| `skills_required` | JSONField | ["Python", "Django"] |
| `salary_min/max` | DecimalField | Compensation range |
| `currency` | CharField | USD, KES, GBP, etc |
| `location` | CharField | Job location |
| `is_remote` | BooleanField | Remote option? |
| `deadline` | DateTimeField | Application deadline |
| `status` | CharField | open/closed/expired/filled |
| `positions_available` | IntegerField | # of spots |
| `is_featured` | BooleanField | Promoted? |

**Key Methods**:
```python
opp.update_view_count()
opp.update_application_count()
opp.increment_positions_filled()
opp.close()                    # Manually close
opp.reopen()                   # Reopen
opp.soft_delete()
opp.can_apply()                # Can students apply?
opp.is_deadline_soon(days=7)
opp.get_salary_display()
```

**Auto Status Updates**:
- 'expired' when deadline passes
- 'filled' when all positions filled
- 'closed' when manually closed

**Searchable/Filterable**:
- By location, employment_type, skills_required
- By is_featured, is_remote
- By deadline

---

## 6. **Application Model** (`apps/applications/models.py`)

**Purpose**: Student applications for opportunities

**Key Fields**:
| Field | Type | Purpose |
|-------|------|---------|
| `student_id` | ForeignKey | Who applied |
| `opportunity_id` | ForeignKey | Applied to |
| `status` | CharField | pending/reviewed/accepted/rejected |
| `cover_letter` | TextField | Student's message |
| `cv_snapshot` | JSONField | CV data at apply time |
| `rating` | IntegerField | Employer rating (1-5) |
| `notes` | TextField | Employer notes |
| `reviewed_by` | ForeignKey(User) | Who reviewed |

**Status Flow**:
```
Student applies
       ↓
pending (waiting for employer review)
       ↓
reviewed (employer reviewing)
       ↓
accepted (offered position) OR rejected (not selected)
```

**Constraints**:
- Unique pair: (student_id, opportunity_id) - prevent duplicates
- Cover letter: 50-2000 characters

**Key Methods**:
```python
app.mark_as_reviewed(reviewer)
app.accept(reviewer, notes='')
app.reject(reviewer, reason='', notes='')
app.withdraw()                 # Student withdraws
app.set_rating(stars, notes='')

# Status checks
app.is_pending
app.is_reviewed
app.is_accepted
app.is_rejected
app.is_active
app.days_since_application
```

**Unique Constraint**: 
- Student cannot apply twice to same opportunity

---

## 7. **FlaggedContent Model** (`apps/admin_panel/models.py`)

**Purpose**: Content moderation for admins

**Reasons for Flagging**:
- spam, inappropriate, scam, duplicate
- low_quality, fake_company, expired
- other

**Status Flow**:
```
pending → reviewed → resolved/dismissed
```

**Actions**:
- warning, remove_content
- suspend_account, ban_account
- restore_content

**Key Methods**:
```python
flag.mark_as_reviewed()
flag.resolve(admin, action='ban_account', notes='')
flag.dismiss(admin)
```

**Constraint**: Either opportunity_id OR employer_id (not both)

---

## 8. **AdminAction Model** (`apps/admin_panel/models.py`)

**Purpose**: Audit log for all admin actions

**Tracked Actions**:
- verify_employer, reject_employer
- ban_user, unban_user
- remove_opportunity, restore_opportunity
- flag_content, dismiss_flag

**Audit Trail**:
- Who performed action
- When it happened
- Which objects were affected
- Description of action

---

## Model Relationships Summary

```
User (1)
  ├── StudentProfile (1:1)
  │   └── Application (1:Many)
  │
  ├── Employer (1:1)
  │   └── Opportunity (1:Many)
  │       └── Application (1:Many)
  │
  ├── AdminUser (1:1)
  │
  ├── administered_flags (1:Many via AdminAction)
  │
  └── reviewed_applications (1:Many via Application.reviewed_by)
```

---

## Database Design Decisions

### 1. **OneToOne Relationships**
- User → StudentProfile: Only students have profiles
- User → Employer: Only employers have employer profiles
- **Cascade delete**: If user deleted → profiles deleted

### 2. **ForeignKey Relationships**
- Employer → Opportunity: One employer posts many opportunities
- **Cascade delete**: If employer deleted → opportunities deleted
- StudentProfile → Application: One student makes many applications
- **Cascade delete**: If student deleted → applications deleted (history)

### 3. **JSON Fields**
```python
# Skills (searchable array)
skills = ["Python", "React", "SQL"]

# CV Snapshot (frozen at application time)
cv_snapshot = {
  "university": "MIT",
  "gpa": 3.85,
  "skills": ["Python", "Django"],
  ...
}
```

### 4. **Unique Constraints**
- `User.email` - No duplicate emails
- `(student_id, opportunity_id)` in Application - No duplicate applications
- Either opportunity OR employer in FlaggedContent - Content moderation

### 5. **Database Indexes**
Created for performance:
- User: email, role, is_active
- StudentProfile: university, profile_complete
- Employer: company_name, is_verified, is_active
- Opportunity: employer+status, location, employment_type, deadline
- Application: student+status, opportunity+status, status, applied_at
- FlaggedContent: status, reason, created_at

---

## Validation Built-In

### User Validation
- Email format check
- Role must be valid choice
- Cannot be both active and inactive (obvious)

### StudentProfile Validation
- GPA must be 0.00-4.00
- Skills must be JSON array with at least 1 item
- CV file must be PDF/DOCX, max 5MB
- User must have role='student'

### Employer Validation
- Company name min 2 characters
- Description min 10 characters
- Cannot be both banned and active
- User must have role='employer'

### Opportunity Validation
- Title min 5 characters
- Description min 50 characters
- Deadline must be future date
- Min salary <= max salary
- At least 1 position available
- At least 1 skill required
- Positions filled <= positions available

### Application Validation
- Cover letter 50-2000 characters
- Cannot apply twice to same opportunity
- Cannot apply to closed opportunities
- Rating must be 1-5 if provided

---

## Business Logic Methods

### Employer can post if:
```python
employer.can_post_opportunities()
# = is_verified AND is_active AND not is_banned AND user.is_active
```

### Student can apply if:
```python
student.can_apply
# = email_verified AND cv_file AND has_skills
```

### Opportunity can accept applications if:
```python
opportunity.can_apply()
# = status=='open' AND deadline>now AND positions<max AND not_deleted
```

### Application status flow:
```python
pending → reviewed → (accepted OR rejected)
```

---

## Usage Examples

### Creating a Student
```python
# Create user
user = User.objects.create(
    email='john@uni.edu',
    password='hashedpass',
    role='student'
)

# Create student profile
profile = StudentProfile.objects.create(
    user=user,
    university='MIT',
    gpa=3.85,
    skills=['Python', 'React', 'SQL'],
    cv_file=cv_file_object
)

# Check if can apply
if profile.can_apply:
    # Can apply for opportunities
```

### Creating an Opportunity
```python
# Create opportunity
opp = Opportunity.objects.create(
    employer=employer,
    title='Python Developer Internship',
    description='We are looking for...',
    skills_required=['Python', 'Django', 'SQL'],
    deadline=future_date,
    positions_available=5
)

# Check status
if opp.can_apply():
    # Show on job board
```

### Applying for Opportunity
```python
# Create application
app = Application.objects.create(
    student=student_profile,
    opportunity=opportunity,
    cover_letter='I am interested because...'
)

# Employer reviews
app.mark_as_reviewed(employer_user)

# Employer decides
app.accept(employer_user, notes='Great candidate')
# or
app.reject(employer_user, reason='Overqualified')
```

### Moderating Content
```python
# Flag inappropriate opportunity
flag = FlaggedContent.objects.create(
    opportunity=opportunity,
    reason='inappropriate',
    description='Uses discriminatory language',
    flagged_by=student_user
)

# Admin reviews and takes action
flag.resolve(
    admin_user,
    action='remove_content',
    notes='Removed for policy violation'
)
```

---

## Next Steps

1. ✅ Models designed and implemented
2. ⏭️ Run migrations: `python manage.py makemigrations`
3. ⏭️ Apply migrations: `python manage.py migrate`
4. ⏭️ Create Django admin interface
5. ⏭️ Create serializers for API endpoints
6. ⏭️ Create views/viewsets for API
7. ⏭️ Create tests for models
8. ⏭️ Add signals for automatic updates (e.g., email notifications)

---

## File Locations

| Model | File |
|-------|------|
| User, AdminUser | `backend/apps/users/models.py` |
| StudentProfile | `backend/apps/students/models.py` |
| Employer | `backend/apps/employers/models.py` |
| Opportunity | `backend/apps/opportunities/models.py` |
| Application | `backend/apps/applications/models.py` |
| FlaggedContent, AdminAction | `backend/apps/admin_panel/models.py` |

---

## Key Production Features Included

✅ **Validation**: Input validation in `clean()` and `save()`
✅ **Relationships**: Proper ForeignKey and OneToOne with cascades
✅ **Indexes**: Database indexes for query performance
✅ **Constraints**: Unique and check constraints
✅ **Business Logic**: Methods for common operations
✅ **Status Tracking**: Auto-updating status based on conditions
✅ **Audit Trail**: Timestamps and tracking of who did what
✅ **Soft Deletes**: Opportunities kept for history
✅ **Docstrings**: Every model and method documented
✅ **Type Hints**: Clear parameter and return types

---

## Notes for Development

### When Running Migrations
```bash
# Create migrations
python manage.py makemigrations

# Check migration plan
python manage.py sqlmigrate apps users 0001

# Apply migrations
python manage.py migrate
```

### When Creating Fixtures (for testing)
Create a file like `backend/apps/users/fixtures/users.json`:
```json
[
  {
    "model": "users.user",
    "pk": 1,
    "fields": {
      "email": "john@example.com",
      "password": "hashed_password",
      "role": "student",
      "is_active": true
    }
  }
]
```

### Database Connection
Models use default Django `default` database (configured in settings)

---

All models are production-ready with:
- Comprehensive validation
- Business logic methods
- Proper relationships
- Performance indexes
- Audit trails
- Clear documentation

