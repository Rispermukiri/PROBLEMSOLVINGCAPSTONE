import React from 'react';

interface CardProps {
  title?: string;
  description?: string;
  footer?: React.ReactNode;
  className?: string;
  children: React.ReactNode;
}

export const Card: React.FC<CardProps> = ({
  title,
  description,
  footer,
  className = '',
  children,
}) => {
  return (
    <div className={`rounded-3xl border border-slate-200 bg-white shadow-sm ${className}`}>
      <div className="space-y-3 p-6">
        {title ? <h2 className="text-xl font-semibold text-slate-900">{title}</h2> : null}
        {description ? <p className="text-sm text-slate-600">{description}</p> : null}
        <div>{children}</div>
      </div>
      {footer ? <div className="rounded-b-3xl border-t border-slate-200 bg-slate-50 p-4">{footer}</div> : null}
    </div>
  );
};
