export type EmployerMetric = {
  label: string;
  value: number;
  trend?: string;
  color: 'blue' | 'emerald' | 'amber' | 'rose';
};

export type PostedOpportunity = {
  id: number;
  title: string;
  status: 'open' | 'closed' | 'filled' | 'expired';
  applicants: number;
  views: number;
  deadline: string;
};

export type QuickAction = {
  label: string;
  description: string;
  buttonText: string;
  href: string;
};
