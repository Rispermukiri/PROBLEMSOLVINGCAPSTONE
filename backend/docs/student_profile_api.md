# Student Profile API Documentation

This document describes the student profile endpoints for AttachLink.
The module follows clean architecture principles by separating:

- Domain logic in `apps/students/models.py`
- Serialization and validation in `apps/students/serializers.py`
- Application use cases in `apps/students/services.py`
- Access control in `apps/students/permissions.py`
- HTTP routing and API behavior in `apps/students/views.py`

## Endpoints

### GET `/api/v1/students/profile/`

Retrieve the authenticated student's profile.

- Authentication: required
- Authorization: student only
- Response: `StudentProfileSerializer`

Response fields:

- `id`
- `user`
  - `id`
  - `email`
  - `role`
- `university`
- `major_field`
- `gpa`
- `graduation_year`
- `bio`
- `phone`
- `skills`
- `cv_file`
- `cv_uploaded_at`
- `is_international`
- `availability_start`
- `preferred_locations`
- `preferred_roles`
- `profile_complete`
- `created_at`
- `updated_at`
- `last_profile_update`

### PUT `/api/v1/students/profile/`

Update the authenticated student's profile.

- Authentication: required
- Authorization: student only
- Request body: all updatable student profile fields
- Supports multipart form data for `cv_file`
- Response: full updated student profile

Example request body:

```json
{
  "university": "Tech University",
  "major_field": "Computer Science",
  "gpa": "3.80",
  "graduation_year": 2026,
  "bio": "Aspiring software engineer.",
  "phone": "+254700000000",
  "skills": ["Python", "Django", "React"],
  "preferred_locations": ["Nairobi", "Remote"],
  "preferred_roles": ["Backend Developer", "Internship"]
}
```

### PATCH `/api/v1/students/profile/`

Partial update of the authenticated student's profile.

- Authentication: required
- Authorization: student only
- Request body: only fields to update

### GET `/api/v1/students/profile/<student_id>/`

Retrieve a public student profile for employers and admins.

- Authentication: required
- Authorization: employer or admin only
- Response: `PublicStudentProfileSerializer`

Response fields:

- `id`
- `user`
  - `id`
  - `email`
  - `role`
- `university`
- `major_field`
- `gpa`
- `graduation_year`
- `bio`
- `skills`
- `preferred_locations`
- `preferred_roles`
- `is_international`
- `availability_start`
- `profile_complete`
- `created_at`

## Validation rules

- `university`: required, non-empty string
- `gpa`: decimal between 0.00 and 4.00
- `skills`, `preferred_locations`, `preferred_roles`: JSON arrays of strings
- `cv_file`: PDF, DOC, or DOCX when uploaded
- `profile_complete`: computed automatically by the model

## Notes

- Student profiles are created automatically when a new student user is registered.
- The profile completeness flag is recalculated on every save.
- Public student profiles do not expose private contact information or CV file contents.

## Documentation UI

Swagger UI is available at `/api/v1/docs/` and OpenAPI schema at `/api/v1/schema/`.
