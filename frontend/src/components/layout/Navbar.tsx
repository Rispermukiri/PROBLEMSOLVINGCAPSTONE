import React, { useState } from 'react';
import { Link, NavLink } from 'react-router-dom';

interface NavLinkItem {
  label: string;
  path: string;
}

interface NavbarProps {
  brand: string;
  links: NavLinkItem[];
  user?: {
    name: string;
    role: string;
  };
  onLogout?: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ brand, links, user, onLogout }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <header className="sticky top-0 z-40 border-b border-slate-200 bg-white shadow-sm">
      <div className="mx-auto flex max-w-screen-2xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        <Link to="/" className="text-xl font-semibold text-slate-900">
          {brand}
        </Link>

        <button
          type="button"
          className="inline-flex items-center rounded-lg border border-slate-200 bg-white p-2 text-slate-700 hover:bg-slate-100 lg:hidden"
          onClick={() => setIsOpen(!isOpen)}
          aria-label="Toggle navigation"
        >
          <span className="sr-only">Open menu</span>
          <svg className="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>

        <nav className={`flex-1 items-center justify-end gap-4 lg:flex ${isOpen ? 'block' : 'hidden'}`}>
          <div className="flex flex-col gap-2 lg:flex-row lg:items-center">
            {links.map((link) => (
              <NavLink
                key={link.path}
                to={link.path}
                className={({ isActive }) =>
                  `rounded-lg px-4 py-2 text-sm font-medium transition ${
                    isActive ? 'bg-slate-100 text-slate-900' : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                  }`
                }
                onClick={() => setIsOpen(false)}
              >
                {link.label}
              </NavLink>
            ))}
          </div>

          <div className="mt-4 flex items-center gap-3 border-t border-slate-200 pt-4 lg:mt-0 lg:border-none lg:pt-0">
            {user ? (
              <>
                <span className="text-sm text-slate-600">{user.name}</span>
                <button
                  type="button"
                  onClick={onLogout}
                  className="rounded-lg bg-slate-100 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-200"
                >
                  Logout
                </button>
              </>
            ) : (
              <Link
                to="/auth/login"
                className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
              >
                Sign in
              </Link>
            )}
          </div>
        </nav>
      </div>
    </header>
  );
};
