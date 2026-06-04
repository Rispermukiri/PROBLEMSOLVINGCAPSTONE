import React from 'react';
import { Card } from '../../../components/common/Card';

interface ApplicationStatusCardProps {
  activeApplications: number;
  statuses: Array<{ label: string; value: number; className: string }>;
}

export const ApplicationStatusCard: React.FC<ApplicationStatusCardProps> = ({ activeApplications, statuses }) => {
  return (
    <Card className="space-y-5" title="Application Status" description="Track your current application pipeline and next steps.">
      <div className="grid gap-4 md:grid-cols-3">
        <div className="rounded-3xl bg-slate-50 p-5 text-center">
          <p className="text-sm uppercase tracking-[0.2em] text-slate-500">Active Applications</p>
          <p className="mt-3 text-4xl font-semibold text-slate-900">{activeApplications}</p>
        </div>
        {statuses.map((status) => (
          <div key={status.label} className={`rounded-3xl p-5 ${status.className}`}>
            <p className="text-sm uppercase tracking-[0.2em] text-white/80">{status.label}</p>
            <p className="mt-3 text-3xl font-semibold text-white">{status.value}</p>
          </div>
        ))}
      </div>
    </Card>
  );
};
