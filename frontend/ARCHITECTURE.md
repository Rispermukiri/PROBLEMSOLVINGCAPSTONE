# AttachLink Frontend Architecture

This document describes a scalable React architecture for AttachLink using React Router, Axios, and Tailwind CSS.

## Recommended folder structure

frontend/
├── public/
│   └── index.html
├── src/
│   ├── assets/                # Static assets such as images, icons, fonts
│   ├── components/            # Shared UI components used across the app
│   │   ├── common/            # Generic atoms and reusable UI pieces
   │   └── layout/            # Layout components like header, footer, sidebar, nav
│   ├── constants/             # App-level constants, route names, statuses, enums
│   ├── context/               # React context providers for auth, theme, app state
│   ├── features/              # Domain feature modules by business capability
   │   ├── admin/              # Admin dashboard screens and feature state
   │   ├── applications/       # Application workflow (apply, list, review)
   │   ├── auth/               # Login, register, password recovery flows
   │   ├── employer/           # Employer dashboard and opportunity management
   │   ├── opportunities/      # Opportunity browsing and detail pages
   │   └── student/            # Student dashboard, profile and application status
│   ├── hooks/                 # Reusable custom hooks for fetching and state logic
   ├── services/              # API clients, Axios instances, and service wrappers
   ├── styles/                # Tailwind entry and global CSS files
   ├── types/                 # TypeScript types and interfaces
   ├── utils/                 # Utility functions, helpers, and formatters
   ├── App.tsx                # App shell and router entry
   ├── main.tsx               # React entry point
   └── routes.tsx             # Central route definitions

## Directory purpose

### `public/`
- Contains the static HTML shell (`index.html`) and any static assets served directly.
- Use for favicons, robots.txt, and public metadata.

### `src/assets/`
- Store images, logos, SVGs, icon files, and any static media referenced by components.
- Keep this separate from CSS and component logic.

### `src/components/`
- Shared visual building blocks that can be reused across multiple screens.
- `common/`: Buttons, inputs, cards, modals, form controls, skeleton loaders.
- `layout/`: Header, footer, sidebar, page shell, navigation, and route wrappers.

### `src/constants/`
- Store route paths, API endpoints, app statuses, role labels, and other constants.
- Example: `ROUTES = { HOME: '/', LOGIN: '/login', OPPORTUNITIES: '/opportunities' }`.

### `src/context/`
- React context providers such as `AuthProvider`, `NotificationProvider`, and `ThemeProvider`.
- Keeps cross-cutting state separate from feature modules.

### `src/features/`
- Each folder is a vertical domain slice of the app.
- Example features:
  - `auth/`: login, register, forgot password, auth forms, auth pages
  - `student/`: student profile, dashboard, application history
  - `employer/`: opportunity creation, editing, applicant review
  - `opportunities/`: public listings, search, filters, opportunity detail
  - `applications/`: apply flow, application status, employer applicant view
  - `admin/`: admin management interfaces and reporting
- Feature folders should contain components, hooks, pages, and feature-specific state.

### `src/hooks/`
- Shared custom hooks used across the app.
- E.g. `useFetch`, `useAuth`, `useDebounce`, `useModal`, `useFormState`.
- Keeps domain logic decoupled from UI components.

### `src/services/`
- Central Axios client and API functions.
- Example files:
  - `api.ts` — configured Axios instance with JWT interceptors
  - `auth.service.ts` — login, logout, refresh token
  - `student.service.ts` — profile and application APIs
  - `employer.service.ts` — opportunity CRUD APIs
  - `opportunity.service.ts` — search and listing APIs
- This is the clean boundary between UI and backend.

### `src/styles/`
- Tailwind CSS configuration import and global styles.
- Example: `index.css`, `tailwind.css`, and theme styles.
- Use Tailwind utility classes in components and keep custom CSS minimal.

### `src/types/`
- TypeScript interfaces and types for API payloads, models, and component props.
- Example: `User.ts`, `Opportunity.ts`, `Application.ts`, `Auth.ts`.

### `src/utils/`
- Helper utilities for formatting dates, currency, validation, routing, and string helpers.
- Example: `formatDate.ts`, `camelToTitle.ts`, `storage.ts`, `auth.ts`.

### `src/App.tsx`
- Mounts the router, global providers, and layout wrappers.
- Minimal logic; delegates page rendering to route components.

### `src/routes.tsx`
- Central route definitions using React Router.
- Example with role-based route protection:
  - `/login`
  - `/register`
  - `/opportunities`
  - `/opportunities/:id`
  - `/student/dashboard`
  - `/employer/dashboard`
  - `/employer/opportunities/new`
- Use route guards such as `ProtectedRoute` and `RoleRoute`.

### `src/main.tsx`
- App entry point that renders `<App />` and wraps it with `BrowserRouter` and providers.

## React Router strategy

- Use a nested route structure for layout separation.
- Example:
  - `/` → public home
  - `/auth/*` → auth pages
  - `/opportunities/*` → public opportunity browsing
  - `/student/*` → student-only area
  - `/employer/*` → employer-only area
- Implement `ProtectedRoute` and `RoleRoute` components in `src/components/layout/` or `src/utils/router.ts`.

## Axios strategy

- Create a shared Axios instance in `src/services/api.ts`.
- Add interceptors for:
  - attaching `Authorization: Bearer <token>`
  - refreshing tokens on 401
  - global error handling
- Build service modules for feature-specific endpoints.
- Keep API calls outside components to simplify testing and reuse.

## Tailwind CSS strategy

- Configure Tailwind in `postcss.config.js` / `tailwind.config.js` at the frontend root.
- Import Tailwind base layers in `src/styles/index.css`.
- Use utility-first classes in components and keep custom CSS for layout / global theming.
- Use component variants and responsive utilities for consistent design.

## Scalable architecture principles

- Keep pages thin and delegate behavior to hooks/services.
- Group code by feature, not by type, to improve maintainability.
- Use shared components for cross-cutting UI patterns.
- Centralize API and auth logic in `services/` and `context/`.
- Use TypeScript types and interfaces to document contracts.

## Example folder summary

- `src/components/`: reusable building blocks
- `src/context/`: global app state providers
- `src/features/`: domain modules for auth, student, employer, opportunities, applications
- `src/hooks/`: custom logic hooks
- `src/services/`: backend API clients and business operations
- `src/styles/`: Tailwind and global CSS
- `src/types/`: type definitions
- `src/utils/`: utility helpers

This structure supports AttachLink growth by isolating business domains, enabling role-based routing, and keeping the backend API surface separate through Axios-backed services.