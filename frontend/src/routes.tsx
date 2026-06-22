import { Link, Navigate, Route, Routes } from 'react-router-dom';
import { Navbar } from './components/layout/Navbar';
import { EmployerDashboard } from './features/employer/pages';
import { StudentDashboard } from './features/student/pages';

const navLinks = [
  { label: 'Student', path: '/student/dashboard' },
  { label: 'Employer', path: '/employer/dashboard' },
];

const HomePage = () => {
  return (
    <main className="min-h-screen bg-slate-50 px-4 py-10 sm:px-6 lg:px-8">
      <div className="mx-auto grid max-w-screen-xl gap-6 lg:grid-cols-[0.9fr_1.1fr] lg:items-center">
        <section className="space-y-5">
          <p className="text-sm font-semibold uppercase text-blue-700">AttachLink</p>
          <h1 className="text-4xl font-semibold text-slate-950 sm:text-5xl">Build the attachment workflow from here.</h1>
          <p className="max-w-2xl text-base leading-7 text-slate-600">
            Start with the student and employer dashboards, then connect each workflow to the Django API as the platform grows.
          </p>
          <div className="flex flex-wrap gap-3">
            <Link
              to="/student/dashboard"
              className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-700"
            >
              Student Dashboard
            </Link>
            <Link
              to="/employer/dashboard"
              className="rounded-md border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-900 transition hover:bg-slate-100"
            >
              Employer Dashboard
            </Link>
          </div>
        </section>

        <section className="grid gap-4 sm:grid-cols-2">
          <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-900">Students</h2>
            <p className="mt-2 text-sm leading-6 text-slate-600">Track profile progress, applications, and recommended opportunities.</p>
          </div>
          <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-900">Employers</h2>
            <p className="mt-2 text-sm leading-6 text-slate-600">Review metrics, postings, applicants, and quick employer actions.</p>
          </div>
        </section>
      </div>
    </main>
  );
};

const AppShell = ({ children }: { children: React.ReactNode }) => {
  return (
    <>
      <Navbar brand="AttachLink" links={navLinks} />
      {children}
    </>
  );
};

export const AppRoutes = () => {
  return (
    <Routes>
      <Route
        path="/"
        element={
          <AppShell>
            <HomePage />
          </AppShell>
        }
      />
      <Route
        path="/student/dashboard"
        element={
          <AppShell>
            <StudentDashboard />
          </AppShell>
        }
      />
      <Route
        path="/employer/dashboard"
        element={
          <AppShell>
            <EmployerDashboard />
          </AppShell>
        }
      />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};
