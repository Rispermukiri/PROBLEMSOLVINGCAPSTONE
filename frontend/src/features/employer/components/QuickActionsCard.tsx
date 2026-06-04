import React from 'react';
import { Link } from 'react-router-dom';
import { QuickAction } from '../types';
import { Button } from '../../../components/common/Button';

export const QuickActionsCard: React.FC<{ actions: QuickAction[] }> = ({ actions }) => {
  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">Quick actions</p>
          <h2 className="mt-2 text-2xl font-semibold text-slate-900">Move faster with employer tools.</h2>
        </div>
      </div>
      <div className="mt-6 space-y-4">
        {actions.map((action) => (
          <div key={action.href} className="rounded-3xl border border-slate-200 p-5">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="font-semibold text-slate-900">{action.label}</p>
                <p className="mt-2 text-sm text-slate-600">{action.description}</p>
              </div>
              <Link to={action.href}>
                <Button variant="primary" size="sm">{action.buttonText}</Button>
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
