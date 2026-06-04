import { useMemo } from 'react';
import { EmployerMetric, PostedOpportunity, QuickAction } from '../types';

export const useEmployerDashboard = () => {
  return useMemo(() => {
    const metrics: EmployerMetric[] = [
      { label: 'Live Opportunities', value: 12, trend: '+8% this week', color: 'blue' },
      { label: 'New Applicants', value: 34, trend: '+15% this week', color: 'emerald' },
      { label: 'Interviews Scheduled', value: 6, trend: 'Stable', color: 'amber' },
      { label: 'Offers Sent', value: 4, trend: '+25%', color: 'rose' },
    ];

    const postedOpportunities: PostedOpportunity[] = [
      {
        id: 1901,
        title: 'Backend Software Internship',
        status: 'open',
        applicants: 18,
        views: 1_245,
        deadline: '2026-06-10',
      },
      {
        id: 1887,
        title: 'UI/UX Designer Attachment',
        status: 'open',
        applicants: 12,
        views: 934,
        deadline: '2026-06-18',
      },
      {
        id: 1862,
        title: 'Data Analytics Internship',
        status: 'filled',
        applicants: 26,
        views: 1_812,
        deadline: '2026-05-31',
      },
    ];

    const quickActions: QuickAction[] = [
      {
        label: 'Publish new opportunity',
        description: 'Create a new internship or attachment listing quickly.',
        buttonText: 'Post Opportunity',
        href: '/employer/opportunities/new',
      },
      {
        label: 'Review applicants',
        description: 'See new submissions and move candidates forward.',
        buttonText: 'View Applicants',
        href: '/employer/applications',
      },
      {
        label: 'Update company profile',
        description: 'Keep your employer profile verified and attractive.',
        buttonText: 'Edit Profile',
        href: '/employer/profile',
      },
    ];

    return { metrics, postedOpportunities, quickActions };
  }, []);
};
