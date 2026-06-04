import React from 'react';
import { Card } from '../../../components/common/Card';
import { ApplicationSummary } from '../types';

interface RecentApplicationsProps {
  applications: ApplicationSummary[];
}

const statusStyles: Record<string, string> = {
  pending: 'bg-yellow-100 text-yellow-800',
  reviewed: 'bg-sky-100 text-sky-700',
  accepted: 'bg-emerald-100 text-emerald-700',
  rejected: 'bg-rose-100 text-rose-700',
  withdrawn: 'bg-slate-100 text-slate-700',
};

export const RecentApplications: React.FC<RecentApplicationsProps> = ({ applications }) => {
  return (
    <Card className="space-y-5" title="Recent Applications" description="Review your latest internship submissions and status updates.">
      <div className="space-y-4">
        {applications.map((application) => (
          <div key={application.id} className="rounded-3xl border border-slate-200 bg-slate-50 p-5">
            <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
              <div>
                <p className="text-lg font-semibold text-slate-900">{application.title}</p>
                <p className="text-sm text-slate-600">{application.employer}</p>
              </div>
              <div className="flex flex-wrap items-center gap-3">
                <span className={`rounded-full px-3 py-1 text-sm font-semibold ${statusStyles[application.status]}`}>
                  {application.statusLabel}
                </span>
                <span className="text-sm text-slate-500">Applied {application.appliedAt}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
};
