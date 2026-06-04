import React from 'react';
import { ProfileCompletionCard } from '../components/ProfileCompletionCard';
import { ApplicationStatusCard } from '../components/ApplicationStatusCard';
import { RecentApplications } from '../components/RecentApplications';
import { InternshipRecommendations } from '../components/InternshipRecommendations';
import { useStudentDashboard } from '../hooks/useStudentDashboard';
import { Button } from '../../../components/common/Button';

export const StudentDashboard: React.FC = () => {
  const { profileCompletion, profileStatus, activeApplications, recentApplications, recommendedOpportunities } = useStudentDashboard();

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-8 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-screen-2xl space-y-8">
        <section className="grid gap-6 xl:grid-cols-[1.4fr_0.9fr]">
          <div className="space-y-6">
            <div className="rounded-3xl bg-white p-8 shadow-sm">
              <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                <div>
                  <p className="text-sm font-semibold uppercase tracking-[0.3em] text-blue-600">Student Dashboard</p>
                  <h1 className="mt-3 text-3xl font-semibold text-slate-900">Welcome back, Esther</h1>
                  <p className="mt-2 text-sm text-slate-600">Here is your latest internship activity and personalized recommendations.</p>
                </div>
                <div className="flex flex-wrap items-center gap-3">
                  <Button variant="primary">Update Profile</Button>
                  <Button variant="secondary">Browse Opportunities</Button>
                </div>
              </div>
            </div>

            <div className="grid gap-6 lg:grid-cols-2">
              <ProfileCompletionCard completion={profileCompletion} detail={profileStatus} />
              <ApplicationStatusCard
                activeApplications={activeApplications}
                statuses={[
                  { label: 'Pending', value: 2, className: 'bg-yellow-500' },
                  { label: 'Reviewed', value: 1, className: 'bg-sky-500' },
                  { label: 'Accepted', value: 1, className: 'bg-emerald-500' },
                ]}
              />
            </div>

            <RecentApplications applications={recentApplications} />
          </div>

          <div className="space-y-6">
            <InternshipRecommendations recommendations={recommendedOpportunities} />
            <div className="rounded-3xl border border-dashed border-slate-200 bg-white p-8 text-center shadow-sm">
              <span className="inline-flex items-center rounded-full bg-blue-50 px-3 py-1 text-sm font-semibold text-blue-700">Tip</span>
              <h2 className="mt-4 text-2xl font-semibold text-slate-900">Improve your odds</h2>
              <p className="mt-3 text-sm leading-6 text-slate-600">
                Complete your profile, add more skills, and upload a polished CV to receive better internship suggestions and faster employer responses.
              </p>
              <Button className="mt-6" variant="primary">Complete profile checklist</Button>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
};
