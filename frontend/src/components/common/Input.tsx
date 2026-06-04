import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  helperText?: string;
  error?: string;
}

export const Input: React.FC<InputProps> = ({
  label,
  helperText,
  error,
  className = '',
  ...props
}) => {
  return (
    <label className="block w-full">
      {label ? <span className="mb-2 block text-sm font-medium text-slate-700">{label}</span> : null}
      <input
        className={`
          w-full rounded-lg border px-4 py-3 text-slate-900 shadow-sm transition duration-150
          focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200
          ${error ? 'border-red-300 bg-red-50 text-red-900' : 'border-slate-300 bg-white'}
          ${className}
        `}
        {...props}
      />
      {helperText ? <p className="mt-2 text-sm text-slate-500">{helperText}</p> : null}
      {error ? <p className="mt-1 text-sm text-red-600">{error}</p> : null}
    </label>
  );
};
