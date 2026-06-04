import React from 'react';
import { MetricCard } from '../components/MetricCard';
import { PostedOpportunityCard } from '../components/PostedOpportunityCard';
import { QuickActionsCard } from '../components/QuickActionsCard';
import { useEmployerDashboard } from '../hooks/useEmployerDashboard';
import { Button } from '../../../components/common/Button';

export const EmployerDashboard: React.FC = () => {
  const { metrics, postedOpportunities, quickActions } = useEmployerDashboard();

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-8 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-screen-2xl space-y-8">
        <section className="rounded-3xl bg-white p-8 shadow-sm">
          <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Employer Dashboard</p>
              <h1 className="mt-3 text-3xl font-semibold text-slate-900">Hi, Jonathan</h1>
              <p className="mt-2 text-sm leading-6 text-slate-600">Monitor your opportunity performance and respond quickly to top applicants.</p>
            </div>
            <div className="flex flex-wrap items-center gap-3">
              <Button variant="primary">Post new opportunity</Button>
              <Button variant="secondary">View applicants</Button>
            </div>
          </div>
        </section>

        <section className="grid gap-6 xl:grid-cols-4">
          {metrics.map((metric) => (
            <MetricCard key={metric.label} metric={metric} />
          ))}
        </section>

        <section className="grid gap-6 xl:grid-cols-[1.4fr_0.9fr]">
          <div className="space-y-6">
            <div className="rounded-3xl bg-white p-6 shadow-sm">
              <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
                <div>
                  <h2 className="text-2xl font-semibold text-slate-900">Posted Opportunities</h2>
                  <p className="mt-2 text-sm text-slate-600">Manage your active and recent internship postings.</p>
                </div>
                <Button variant="secondary">See all postings</Button>
              </div>
              <div className="mt-6 space-y-4">
                {postedOpportunities.map((opportunity) => (
                  <PostedOpportunityCard key={opportunity.id} opportunity={opportunity} />
                ))}
              </div>
            </div>
          </div>

          <QuickActionsCard actions={quickActions} />
        </section>
      </div>
    </main>
  );
};
