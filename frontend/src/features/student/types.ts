export type ApplicationSummary = {
  id: number;
  title: string;
  employer: string;
  status: 'pending' | 'reviewed' | 'accepted' | 'rejected' | 'withdrawn';
  appliedAt: string;
  statusLabel: string;
};

export type OpportunityRecommendation = {
  id: number;
  title: string;
  employer: string;
  location: string;
  deadline: string;
  matchScore: number;
  employmentType: string;
  remote: boolean;
};

export type StudentDashboardData = {
  profileCompletion: number;
  profileStatus: string;
  activeApplications: number;
  recommendedOpportunities: OpportunityRecommendation[];
  recentApplications: ApplicationSummary[];
};
