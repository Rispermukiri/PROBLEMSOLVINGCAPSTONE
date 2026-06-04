import React from 'react';
import { Card } from '../../../components/common/Card';
import { OpportunityRecommendation } from '../types';
import { Button } from '../../../components/common/Button';

interface InternshipRecommendationsProps {
  recommendations: OpportunityRecommendation[];
}

export const InternshipRecommendations: React.FC<InternshipRecommendationsProps> = ({ recommendations }) => {
  return (
    <Card className="space-y-5" title="Recommended Internships" description="These opportunities match your profile and recent activity.">
      <div className="grid gap-4 xl:grid-cols-3">
        {recommendations.map((opportunity) => (
          <div key={opportunity.id} className="space-y-4 rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
            <div className="flex items-center justify-between gap-3">
              <div>
                <p className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">{opportunity.employmentType}</p>
                <h3 className="mt-2 text-lg font-semibold text-slate-900">{opportunity.title}</h3>
              </div>
              <div className="rounded-2xl bg-slate-100 px-3 py-1 text-sm text-slate-700">
                {opportunity.remote ? 'Remote' : 'On-site'}
              </div>
            </div>
            <div className="space-y-2 text-sm text-slate-600">
              <p>{opportunity.employer}</p>
              <p>{opportunity.location}</p>
              <p>Deadline: {opportunity.deadline}</p>
            </div>
            <div className="flex items-center justify-between gap-3">
              <span className="rounded-full bg-emerald-100 px-3 py-1 text-sm font-semibold text-emerald-700">
                Match {opportunity.matchScore}%
              </span>
              <Button variant="secondary" size="sm">View</Button>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
};
