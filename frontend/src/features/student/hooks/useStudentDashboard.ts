import { useMemo } from 'react';
import { ApplicationSummary, OpportunityRecommendation, StudentDashboardData } from '../types';

export const useStudentDashboard = (): StudentDashboardData => {
  const data = useMemo(() => {
    const recentApplications: ApplicationSummary[] = [
      {
        id: 421,
        title: 'Backend Internship at Atlas Labs',
        employer: 'Atlas Labs',
        status: 'pending',
        statusLabel: 'Pending review',
        appliedAt: '2026-05-28',
      },
      {
        id: 407,
        title: 'Product Design Attachment',
        employer: 'Futura Creative',
        status: 'reviewed',
        statusLabel: 'Under review',
        appliedAt: '2026-05-20',
      },
      {
        id: 394,
        title: 'Software Engineer Internship',
        employer: 'Nairobi Tech Hub',
        status: 'accepted',
        statusLabel: 'Offer received',
        appliedAt: '2026-05-10',
      },
    ];

    const recommendedOpportunities: OpportunityRecommendation[] = [
      {
        id: 1482,
        title: 'Full-Stack Internship',
        employer: 'SmartGrid',
        location: 'Nairobi, Kenya',
        deadline: '2026-06-15',
        matchScore: 94,
        employmentType: 'Internship',
        remote: true,
      },
      {
        id: 1519,
        title: 'Data Science Attachment',
        employer: 'Insight Analytics',
        location: 'Remote',
        deadline: '2026-06-20',
        matchScore: 90,
        employmentType: 'Attachment',
        remote: true,
      },
      {
        id: 1544,
        title: 'Frontend Internship',
        employer: 'BrightWorks',
        location: 'Nairobi, Kenya',
        deadline: '2026-06-22',
        matchScore: 88,
        employmentType: 'Internship',
        remote: false,
      },
    ];

    return {
      profileCompletion: 78,
      profileStatus: 'Good progress — keep your profile updated to improve recommendations.',
      activeApplications: recentApplications.length,
      recentApplications,
      recommendedOpportunities,
    };
  }, []);

  return data;
};
