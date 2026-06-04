import React from 'react';
import { PostedOpportunity } from '../types';
import { Button } from '../../../components/common/Button';

const statusClass: Record<PostedOpportunity['status'], string> = {
  open: 'bg-emerald-100 text-emerald-800',
  closed: 'bg-slate-100 text-slate-700',
  filled: 'bg-blue-100 text-blue-800',
  expired: 'bg-rose-100 text-rose-800',
};

export const PostedOpportunityCard: React.FC<{ opportunity: PostedOpportunity }> = ({ opportunity }) => {
  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
        <div>
          <p className="text-lg font-semibold text-slate-900">{opportunity.title}</p>
          <div className="mt-2 flex flex-wrap items-center gap-2 text-sm text-slate-500">
            <span>{opportunity.deadline} deadline</span>
            <span>•</span>
            <span>{opportunity.applicants} applicants</span>
            <span>•</span>
            <span>{opportunity.views} views</span>
          </div>
        </div>
        <span className={`rounded-full px-3 py-1 text-sm font-semibold ${statusClass[opportunity.status]}`}>
          {opportunity.status}
        </span>
      </div>
      <div className="mt-5 flex flex-wrap items-center gap-3">
        <Button variant="secondary" size="sm">Manage</Button>
        <Button variant="ghost" size="sm">View applicants</Button>
      </div>
    </div>
  );
};
