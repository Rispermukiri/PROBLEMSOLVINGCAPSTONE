# AttachLink - Database Design & Models

## Data Model Overview

This document outlines the database schema for AttachLink, including entities, relationships, and key business logic.

---

## Entity Relationship Diagram (ERD)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                    DATABASE SCHEMA - ATTACHLINK                            │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                            USER (Base)                              │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │ PK: id (UUID)                                                      │  │
│  │ • email (VARCHAR, unique)                                          │  │
│  │ • password_hash (VARCHAR)                                          │  │
│  │ • role (ENUM: 'student' | 'employer' | 'admin')                   │  │
│  │ • is_active (BOOLEAN, default=True)                               │  │
│  │ • email_verified (BOOLEAN, default=False)                         │  │
│  │ • created_at (TIMESTAMP)                                          │  │
│  │ • updated_at (TIMESTAMP)                                          │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│              ↑                    ↑                    ↑                    │
│              │ (1:1)              │ (1:1)              │ (1:1)              │
│              │ optional           │ optional           │ optional           │
│              │                    │                    │                    │
│  ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────┐  │
│  │ StudentProfile       │  │ Employer             │  │ AdminUser        │  │
│  ├──────────────────────┤  ├──────────────────────┤  ├──────────────────┤  │
│  │ PK: id              │  │ PK: id               │  │ PK: id           │  │
│  │ FK: user_id ────────┼──┼─ (to User.id)       │  │ FK: user_id ──────┼──┼─ (to User.id)
│  │ • university        │  │ • company_name      │  │ • role           │  │
│  │ • gpa               │  │ • company_logo      │  │ (hardcoded admin)│  │
│  │ • bio               │  │ • industry          │  │ • permissions    │  │
│  │ • phone             │  │ • website           │  │ • created_at     │  │
│  │ • cv_file (URL)     │  │ • description       │  └──────────────────┘  │
│  │ • skills (JSON)     │  │ • verified_at       │                        │
│  │ • created_at        │  │ • is_verified       │                        │
│  │ • updated_at        │  │ • created_at        │                        │
│  └──────────────────────┘  │ • updated_at        │                        │
│                            └──────────────────────┘                        │
│                                    ↑                                       │
│                                    │ (1:Many)                              │
│                                    │                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                        Opportunity                                 │  │
│  ├─────────────────────────────────────────────────────────────────────┤  │
│  │ PK: id                                                              │  │
│  │ FK: employer_id (to Employer.id)                                   │  │
│  │ • title (VARCHAR)           - e.g., "Python Developer Internship" │  │
│  │ • description (TEXT)        - Detailed job description            │  │
│  │ • requirements (TEXT/JSON)  - Required qualifications             │  │
│  │ • skills_required (JSON)    - List of required skills             │  │
│  │ • salary_min (DECIMAL)      - Minimum salary/stipend              │  │
│  │ • salary_max (DECIMAL)      - Maximum salary/stipend              │  │
│  │ • currency (VARCHAR)        - 'USD', 'KES', 'GBP', etc            │  │
│  │ • location (VARCHAR)        - Office location                     │  │
│  │ • employment_type (ENUM)    - 'internship' | 'attachment'         │  │
│  │ • positions_available (INT) - How many positions                  │  │
│  │ • deadline (DATETIME)       - Application deadline                │  │
│  │ • status (ENUM)             - 'open'|'closed'|'expired'|'filled'  │  │
│  │ • is_featured (BOOLEAN)     - Promoted opportunity                │  │
│  │ • created_at (DATETIME)                                           │  │
│  │ • updated_at (DATETIME)                                           │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                    ↑                                       │
│                                    │ (1:Many)                              │
│                                    │                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                        Application                                 │  │
│  ├─────────────────────────────────────────────────────────────────────┤  │
│  │ PK: id                                                              │  │
│  │ FK: student_id (to StudentProfile.id)  (1:Many from StudentProfile│  │
│  │ FK: opportunity_id (to Opportunity.id) (1:Many from Opportunity)  │  │
│  │ FK: reviewed_by (to User.id, nullable) - Admin/Employer reviewer   │  │
│  │ Unique constraint: (student_id, opportunity_id)                    │  │
│  │                                                                     │  │
│  │ • status (ENUM)        - 'pending'|'reviewed'|'accepted'|'rejected'   │
│  │ • cover_letter (TEXT)  - Student's application message            │  │
│  │ • cv_snapshot (JSON)   - Store CV on application for history      │  │
│  │ • rating (INT 1-5)     - Employer rating of applicant             │  │
│  │ • notes (TEXT)         - Employer notes on application            │  │
│  │ • applied_at (DATETIME)                                           │  │
│  │ • reviewed_at (DATETIME, nullable)                                │  │
│  │ • decided_at (DATETIME, nullable) - When accept/reject happened   │  │
│  │ • created_at (DATETIME)                                           │  │
│  │ • updated_at (DATETIME)                                           │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                    FlaggedContent (Admin)                          │  │
│  ├─────────────────────────────────────────────────────────────────────┤  │
│  │ PK: id                                                              │  │
│  │ FK: opportunity_id (nullable, to Opportunity.id)                   │  │
│  │ FK: employer_id (nullable, to Employer.id)                        │  │
│  │ FK: flagged_by (to User.id)                                        │  │
│  │                                                                     │  │
│  │ • reason (VARCHAR)        - Why flagged (spam, inappropriate, etc) │  │
│  │ • description (TEXT)      - Details of the flag                   │  │
│  │ • status (ENUM)           - 'pending'|'reviewed'|'resolved'        │  │
│  │ • resolution (TEXT)       - Admin's action taken                  │  │
│  │ • created_at (DATETIME)                                           │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Relationships Explained

### 1. **User → StudentProfile (1:1, Optional)**

```
One User can have at most one StudentProfile
One StudentProfile belongs to exactly one User

Why optional?
- User might be employer or admin (not student)
- StudentProfile created only if user.role == 'student'
```

**Cascade behavior**: If User is deleted → StudentProfile is deleted


### 2. **User → Employer (1:1, Optional)**

```
One User can have at most one Employer profile
One Employer belongs to exactly one User

Why optional?
- User might be student or admin (not employer)
- Employer created only if user.role == 'employer'
```

**Cascade behavior**: If User is deleted → Employer profile is deleted


### 3. **Employer → Opportunity (1:Many)**

```
One Employer can post many Opportunities
One Opportunity belongs to exactly one Employer

Examples:
- "Google" (1 Employer) posts:
  - "Python Developer Internship" (Opportunity 1)
  - "Data Science Attachment" (Opportunity 2)
  - "Frontend Developer Internship" (Opportunity 3)
```

**Cascade behavior**: If Employer is deleted → All their Opportunities deleted


### 4. **StudentProfile → Application (1:Many)**

```
One Student can apply for many Opportunities
One Application belongs to exactly one Student

Examples:
- "John" (1 StudentProfile) applies for:
  - "Python Developer Internship" at Google (Application 1)
  - "Data Science Internship" at Microsoft (Application 2)
  - "Frontend Developer" at Apple (Application 3)
```

**Cascade behavior**: If StudentProfile deleted → Applications are kept (historical record) OR deleted (configurable)


### 5. **Opportunity → Application (1:Many)**

```
One Opportunity can have many Applicants
One Application is for exactly one Opportunity

Examples:
- "Python Developer Internship" at Google gets:
  - John's application (Application 1)
  - Sarah's application (Application 2)
  - Mike's application (Application 3)
```

**Cascade behavior**: If Opportunity deleted → Applications kept (soft delete recommended)


### 6. **User → Application.reviewed_by (1:Many, Optional)**

```
One User (Employer/Admin) can review many Applications
One Application can be reviewed by one User (optional - null initially)

Examples:
- Jane (Employer) reviews:
  - John's application (reviewed_by = Jane)
  - Sarah's application (reviewed_by = Jane)
```

**Usage**: Tracks who reviewed/decided on each application


---

## Entity Descriptions

### **User**

**Purpose**: Base authentication model for all users

**Attributes**:
| Field | Type | Purpose | Notes |
|-------|------|---------|-------|
| `id` | UUID/AutoField | Primary key | Auto-generated |
| `email` | CharField(unique) | Login identifier | Must be unique |
| `password_hash` | CharField | Encrypted password | Never store plain text |
| `role` | CharField(choices) | User type | 'student' \| 'employer' \| 'admin' |
| `is_active` | BooleanField | Account status | For soft-delete or deactivation |
| `email_verified` | BooleanField | Email confirmation status | For email verification flow |
| `created_at` | DateTimeField(auto_now_add) | Account creation | Auto-set on create |
| `updated_at` | DateTimeField(auto_now) | Last update | Auto-updated |

**Business Rules**:
- Email must be unique across all users
- Password must be hashed (never stored plain)
- Role determines what profile is created
- Email verification required before full access
- One email per account (no duplicates)


### **StudentProfile**

**Purpose**: Stores additional student-specific information

**Attributes**:
| Field | Type | Purpose | Notes |
|-------|------|---------|-------|
| `id` | AutoField | Primary key | |
| `user_id` | OneToOneField(User) | Link to user | Must exist |
| `university` | CharField | School name | e.g., "MIT", "Stanford" |
| `gpa` | DecimalField(3,2) | Grade point avg | e.g., 3.85, range 0.00-4.00 |
| `bio` | TextField | About student | Short biography |
| `phone` | CharField | Contact number | Optional |
| `cv_file` | FileField/URLField | CV document | PDF or DOCX format |
| `skills` | JSONField | Technical skills | e.g., ["Python", "React", "SQL"] |
| `is_international` | BooleanField | Visa status | For filtering |
| `availability_start` | DateField | When available | For internship start date |
| `created_at` | DateTimeField | Profile creation | |
| `updated_at` | DateTimeField | Last update | |

**Business Rules**:
- Only created when user.role == 'student'
- GPA must be between 0.00 and 4.00
- One StudentProfile per Student (OneToOne)
- CV is required before applying (can be updated)
- Skills stored as JSON array for easy filtering


### **Employer**

**Purpose**: Stores company information and employer profile

**Attributes**:
| Field | Type | Purpose | Notes |
|-------|------|---------|-------|
| `id` | AutoField | Primary key | |
| `user_id` | OneToOneField(User) | Link to user | Must exist |
| `company_name` | CharField | Official company name | e.g., "Google LLC" |
| `company_logo` | ImageField | Company logo | For display |
| `industry` | CharField | Business sector | e.g., "Technology", "Finance" |
| `website` | URLField | Company website | For verification & links |
| `description` | TextField | About company | Company description |
| `headquarters_location` | CharField | HQ location | For filtering |
| `is_verified` | BooleanField | Admin verification | Admin must verify before posting |
| `verified_at` | DateTimeField | Verification timestamp | null if not verified |
| `verified_by` | ForeignKey(User) | Admin who verified | Audit trail |
| `created_at` | DateTimeField | Profile creation | |
| `updated_at` | DateTimeField | Last update | |

**Business Rules**:
- Only created when user.role == 'employer'
- Must be verified by admin before posting opportunities
- Cannot post opportunities if is_verified == False
- One Employer profile per company user (OneToOne)
- Logo used in opportunity listings


### **Opportunity**

**Purpose**: Internship/attachment opportunity posting

**Attributes**:
| Field | Type | Purpose | Notes |
|-------|------|---------|-------|
| `id` | AutoField | Primary key | |
| `employer_id` | ForeignKey(Employer) | Posted by | Who created this |
| `title` | CharField | Job title | e.g., "Python Developer Internship" |
| `description` | TextField | Full description | Detailed info about role |
| `requirements` | TextField \| JSONField | Required qualifications | What student needs |
| `skills_required` | JSONField | Technical skills | e.g., ["Python", "Django", "SQL"] |
| `salary_min` | DecimalField | Minimum compensation | In specified currency |
| `salary_max` | DecimalField | Maximum compensation | In specified currency |
| `currency` | CharField | Currency code | "USD", "KES", "GBP", etc |
| `location` | CharField | Job location | City/country where internship is |
| `employment_type` | CharField(choices) | Type | 'internship' \| 'attachment' |
| `duration_weeks` | IntegerField | Length | How many weeks |
| `positions_available` | IntegerField | Open spots | How many can be hired |
| `deadline` | DateTimeField | Application deadline | When applications close |
| `status` | CharField(choices) | Current status | 'open' \| 'closed' \| 'expired' \| 'filled' |
| `is_featured` | BooleanField | Promoted | Show at top of listings |
| `is_remote` | BooleanField | Work from home | Remote option available |
| `created_at` | DateTimeField | Posted date | When posted |
| `updated_at` | DateTimeField | Last update | When last edited |

**Business Rules**:
- Employer must be verified before posting
- Deadline must be in future when created
- Status auto-updates:
  - 'filled' when positions_available reached
  - 'expired' after deadline passes
  - 'closed' when employer manually closes
- Skills are searchable (used in filtering)
- Cannot delete (soft delete for history)


### **Application**

**Purpose**: Track student applications to opportunities

**Attributes**:
| Field | Type | Purpose | Notes |
|-------|------|---------|-------|
| `id` | AutoField | Primary key | |
| `student_id` | ForeignKey(StudentProfile) | Who applied | Student record |
| `opportunity_id` | ForeignKey(Opportunity) | Applied for | Which opportunity |
| `status` | CharField(choices) | Current status | 'pending' \| 'reviewed' \| 'accepted' \| 'rejected' |
| `cover_letter` | TextField | Application message | Student's pitch |
| `cv_snapshot` | JSONField | CV copy | Store CV data at application time |
| `rating` | IntegerField | Employer rating | 1-5 stars (optional) |
| `notes` | TextField | Employer notes | Feedback/comments |
| `applied_at` | DateTimeField | Application date | When student applied |
| `reviewed_at` | DateTimeField | Review start | When employer first reviewed |
| `decided_at` | DateTimeField | Decision date | When accept/reject happened |
| `reviewed_by` | ForeignKey(User, null=True) | Reviewer | Who made decision |
| `created_at` | DateTimeField | Record creation | |
| `updated_at` | DateTimeField | Last update | |

**Indexes & Constraints**:
- Unique constraint: `(student_id, opportunity_id)` - prevent duplicate applications
- Index on `student_id` - for "my applications" queries
- Index on `opportunity_id` - for "who applied" queries
- Index on `status` - for filtering by status
- Index on `applied_at` - for sorting by date

**Business Rules**:
- Student can only apply once per opportunity (unique constraint)
- Application created when student clicks "Apply"
- Status flow: pending → reviewed → accepted/rejected
- Employer can change status and leave notes
- CV snapshot saves student's CV data at application time
- Application history kept even after opportunity closes


### **FlaggedContent**

**Purpose**: Admin moderation - flag inappropriate content

**Attributes**:
| Field | Type | Purpose | Notes |
|-------|------|---------|-------|
| `id` | AutoField | Primary key | |
| `opportunity_id` | ForeignKey(Opportunity, null=True) | What's flagged | Null if flagging employer |
| `employer_id` | ForeignKey(Employer, null=True) | Flagged employer | Null if flagging opportunity |
| `flagged_by` | ForeignKey(User) | Who flagged | For audit trail |
| `reason` | CharField(choices) | Flag reason | 'spam' \| 'inappropriate' \| 'duplicate' \| 'fraud' |
| `description` | TextField | Details | Why it was flagged |
| `status` | CharField(choices) | Resolution | 'pending' \| 'reviewed' \| 'resolved' |
| `resolution` | TextField | Admin action | What admin did |
| `resolved_by` | ForeignKey(User, null=True) | Admin who resolved | |
| `created_at` | DateTimeField | Flagged date | |
| `updated_at` | DateTimeField | Last update | |

**Business Rules**:
- Either opportunity_id OR employer_id must be set (not both)
- Used for content moderation
- Admin reviews and decides action
- Keeps audit trail of moderation activities


---

## Database Design Decisions

### 1. **UUID vs Auto-Increment ID?**

**Decision**: Auto-increment for now, can migrate to UUID later
- **Pros**: Simpler for learning, backward compatible
- **Cons**: Sequential IDs leak usage information
- **When to change**: When privacy is critical or distributed system needed

### 2. **Why Separate StudentProfile and Employer?**

**Answer**: Different data requirements
- Student has: university, GPA, CV, skills
- Employer has: company name, logo, industry, verification
- Separating allows for different fields without wasting space

### 3. **Why ForeignKey cascade?**

**Answer**: Maintain referential integrity
- Delete user → delete their profiles (consistency)
- Delete employer → delete their opportunities (clean up)
- Delete opportunity → keep applications (history)

### 4. **Why unique constraint on (student_id, opportunity_id)?**

**Answer**: Prevent duplicate applications
- Student can't apply twice for same opportunity
- Database enforces business rule
- Reduces validation code

### 5. **JSON Fields vs Separate Tables?**

**Scenarios**:

**Skills (JSON vs Skills Table)**
```
Option 1: JSON Array (CURRENT)
StudentProfile.skills = ["Python", "React", "SQL"]
✅ Simple, denormalized, fast for listing
❌ Hard to query "find students with Python"

Option 2: Separate Table
CREATE TABLE StudentSkills (
  id PK,
  student_id FK,
  skill_id FK,
  proficiency ENUM
)
✅ Queryable, normalized
❌ More complex, more joins
```

**Decision**: JSON for now, upgrade to separate table if need complex skill filtering

### 6. **Soft Delete vs Hard Delete?**

For Opportunities:
- Don't actually delete (soft delete)
- Set `is_deleted = True` or keep for history
- Keep application links valid
- Can restore if needed

For Applications:
- Keep permanently (audit trail)
- Track hiring process

### 7. **Why CV Snapshot in Application?**

**Reason**: Student's CV might change while employer reviews
- Store what CV info was when they applied
- Fair comparison
- Historical accuracy

---

## Data Validation Rules

### User
- Email: Valid email format, unique
- Password: Min 8 chars, 1 uppercase, 1 digit
- Role: Must be one of (student, employer, admin)

### StudentProfile
- University: Required, non-empty
- GPA: Must be 0.00 - 4.00
- Phone: Optional, valid format if provided
- CV File: Required, PDF or DOCX, max 5MB
- Skills: Required, at least 1 skill

### Employer
- Company Name: Required, 3-255 chars
- Industry: Required, from predefined list
- Website: Valid URL format
- Logo: Optional, image format, max 2MB

### Opportunity
- Title: Required, 5-255 chars
- Description: Required, min 50 chars
- Deadline: Must be future date
- Salary Min/Max: Min <= Max if both provided
- Positions: At least 1
- Skills Required: At least 1 skill
- Status: Valid choice from enum

### Application
- Cover Letter: Required, 50-2000 chars
- Status: Valid choice from enum
- Unique pair: (student_id, opportunity_id)

---

## Query Patterns

### Common Queries

#### Students finding opportunities
```sql
SELECT * FROM opportunities 
WHERE status = 'open' 
AND deadline > NOW()
AND skills_required @> '["Python"]'  -- JSON contains
ORDER BY created_at DESC;
```

#### Employer viewing applicants
```sql
SELECT a.*, s.*, u.email 
FROM applications a
JOIN student_profile s ON a.student_id = s.id
JOIN user u ON s.user_id = u.id
WHERE a.opportunity_id = ?
AND a.status IN ('pending', 'reviewed')
ORDER BY a.applied_at DESC;
```

#### Admin moderation
```sql
SELECT * FROM flagged_content
WHERE status = 'pending'
ORDER BY created_at ASC;
```

---

## Next Steps

1. ✅ Schema designed
2. ⏭️ Create Django model classes
3. ⏭️ Add model validation (clean methods)
4. ⏭️ Add model methods (helpers)
5. ⏭️ Create migrations
6. ⏭️ Add admin interface
7. ⏭️ Create fixtures for testing

