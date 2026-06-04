import React from 'react';
import { Card } from '../../../components/common/Card';

interface ProfileCompletionCardProps {
  completion: number;
  detail: string;
}

export const ProfileCompletionCard: React.FC<ProfileCompletionCardProps> = ({ completion, detail }) => {
  return (
    <Card className="space-y-5" title="Profile Completion" description="Keep your student profile strong to increase your match rate and application success.">
      <div className="space-y-4">
        <div className="flex items-center justify-between gap-4">
          <span className="text-3xl font-semibold text-slate-900">{completion}%</span>
          <span className="rounded-full bg-blue-50 px-3 py-1 text-sm font-medium text-blue-700">On track</span>
        </div>
        <div className="h-3 overflow-hidden rounded-full bg-slate-100">
          <div className="h-full rounded-full bg-gradient-to-r from-blue-500 to-cyan-500" style={{ width: `${completion}%` }} />
        </div>
        <p className="text-sm leading-6 text-slate-600">{detail}</p>
      </div>
    </Card>
  );
};
