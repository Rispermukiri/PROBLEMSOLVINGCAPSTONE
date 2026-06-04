# Student Application Workflow API

This document describes the application workflow for AttachLink.
Students can apply for opportunities once per opportunity. Employers can view applicants for their own postings.

## Architecture

- `apps/applications/models.py`: domain model and workflow state
- `apps/applications/serializers.py`: request/response validation and serialization
- `apps/applications/services.py`: application use cases and query logic
- `apps/applications/permissions.py`: authorization rules for students and employers
- `apps/applications/views.py`: HTTP endpoints and workflow orchestration

## Endpoints

### GET `/api/v1/applications/`

List applications for the authenticated user.

- Students: returns their own applications
- Employers: returns applications submitted to their opportunities

### POST `/api/v1/applications/apply/`

Submit an application for an opportunity.

- Authentication: required
- Authorization: student only
- Students may apply only once per opportunity.

Request body:

```json
{
  "opportunity_id": 123,
  "cover_letter": "I am very interested in this internship because..."
}
```

### GET `/api/v1/applications/<application_id>/`

Retrieve application details.

- Authentication: required
- Authorization: student applicant or owning employer

### POST `/api/v1/applications/<application_id>/withdraw/`

Withdraw a pending/reviewed application.

- Authentication: required
- Authorization: student applicant only

## Validation rules

- One application per student per opportunity enforced by:
  - `Application` unique constraint
  - serializer validation
- Cover letter must be 50-2000 characters
- Opportunity must still be open and accepting applications

## Notes

- Employers may view applicants for opportunities they own.
- Application summaries include opportunity and student metadata.
- The application workflow prevents duplicate submissions and enforces role-based access.
