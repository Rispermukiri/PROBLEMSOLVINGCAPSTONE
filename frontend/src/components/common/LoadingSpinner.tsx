import React from 'react';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  label?: string;
  className?: string;
}

const sizeClasses: Record<NonNullable<LoadingSpinnerProps['size']>, string> = {
  sm: 'h-6 w-6 border-2',
  md: 'h-8 w-8 border-4',
  lg: 'h-12 w-12 border-4',
};

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'md',
  label,
  className = '',
}) => {
  return (
    <div className={`flex flex-col items-center justify-center gap-3 ${className}`}>
      <span
        className={`inline-block animate-spin rounded-full border-slate-300 border-t-blue-600 ${sizeClasses[size]}`}
        aria-label={label ?? 'Loading'}
      />
      {label ? <span className="text-sm text-slate-600">{label}</span> : null}
    </div>
  );
};
