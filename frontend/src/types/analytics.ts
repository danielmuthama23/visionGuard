export interface AnalyticsData {
    hourlyData: Array<{ hour: string; count: number }>;
    dailyTrends: Array<{ day: string; vehicleType: string; count: number }>;
    stats: {
      peakHour: string;
      averageStay: string;
      totalRevenue: number;
      nftsMinted: number;
    };
  }