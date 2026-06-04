# Internship Opportunity API Documentation

This document describes the internship opportunity API for AttachLink.
The module follows clean architecture by separating:

- domain models in `apps/opportunities/models.py`
- validation and serialization in `apps/opportunities/serializers.py`
- application services in `apps/opportunities/services.py`
- permissions in `apps/opportunities/permissions.py`
- HTTP controllers in `apps/opportunities/views.py`

## Endpoints

### GET `/api/v1/opportunities/`

List active internship/attachment opportunities.

Query parameters:
- `employment_type`
- `location`
- `is_remote`
- `is_featured`
- `search`
- `page`
- `page_size`

Response: paginated list of opportunities using `OpportunityListSerializer`.

### POST `/api/v1/opportunities/create/`

Create a new opportunity.

- Authentication: required
- Authorization: verified employers only
- Request body fields:
  - `title`
  - `description`
  - `requirements`
  - `responsibilities`
  - `skills_required`
  - `experience_level`
  - `salary_min`
  - `salary_max`
  - `currency`
  - `is_paid`
  - `location`
  - `is_remote`
  - `employment_type`
  - `duration_weeks`
  - `start_date`
  - `deadline`
  - `positions_available`

Response: created opportunity detail.

### GET `/api/v1/opportunities/<opportunity_id>/`

Retrieve opportunity details.

- Authentication: optional
- Authorization: public view
- Response: `OpportunityDetailSerializer`

### PUT/PATCH `/api/v1/opportunities/<opportunity_id>/update/`

Update an existing opportunity.

- Authentication: required
- Authorization: owning employer only
- Request body: any updatable opportunity field

### DELETE `/api/v1/opportunities/<opportunity_id>/delete/`

Soft delete an opportunity.

- Authentication: required
- Authorization: owning employer only

## Validation rules

- `title`: at least 5 characters
- `description`: at least 50 characters
- `skills_required`: non-empty list of strings
- `deadline`: must be in the future
- `salary_max`: must be greater than or equal to `salary_min`
- `positions_available`: integer >= 1

## Notes

- Students may only read opportunity listings and details.
- Employers may create, update, and delete only their own opportunities.
- Employers must be verified and active to create opportunities.
- Deletion is a soft delete; the record remains in the database for audit.
