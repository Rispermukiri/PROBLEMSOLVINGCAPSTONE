import React from 'react';
import { EmployerMetric } from '../types';

const colorClasses: Record<EmployerMetric['color'], string> = {
  blue: 'bg-blue-500 text-white',
  emerald: 'bg-emerald-500 text-white',
  amber: 'bg-amber-500 text-white',
  rose: 'bg-rose-500 text-white',
};

export const MetricCard: React.FC<{ metric: EmployerMetric }> = ({ metric }) => {
  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-sm font-medium uppercase tracking-[0.24em] text-slate-500">{metric.label}</p>
          <p className="mt-3 text-4xl font-semibold text-slate-900">{metric.value}</p>
        </div>
        <span className={`rounded-2xl px-3 py-2 text-sm font-semibold ${colorClasses[metric.color]}`}>
          {metric.trend}
        </span>
      </div>
    </div>
  );
};
