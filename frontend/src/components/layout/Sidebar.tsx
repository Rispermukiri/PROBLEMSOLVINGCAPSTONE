import React from 'react';
import { Link } from 'react-router-dom';

interface SidebarItem {
  label: string;
  path: string;
  icon?: React.ReactNode;
}

interface SidebarProps {
  title?: string;
  items: SidebarItem[];
  className?: string;
  onClose?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ title, items, className = '', onClose }) => {
  return (
    <aside className={`w-full max-w-xs space-y-6 border-r border-slate-200 bg-white p-4 ${className}`}>
      {title ? <div className="text-lg font-semibold text-slate-900">{title}</div> : null}
      <nav className="space-y-1">
        {items.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className="flex items-center gap-3 rounded-2xl px-4 py-3 text-sm font-medium text-slate-700 transition hover:bg-slate-100"
            onClick={onClose}
          >
            {item.icon ? <span className="text-base">{item.icon}</span> : null}
            <span>{item.label}</span>
          </Link>
        ))}
      </nav>
    </aside>
  );
};
