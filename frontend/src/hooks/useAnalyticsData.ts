// src/hooks/useAnalyticsData.ts

import { useQuery } from "@tanstack/react-query";
import { api } from "@/services/api";

interface AnalyticsData {
  hourlyData: Array<{ hour: string; count: number }>;
  dailyTrends: Array<{ day: string; vehicleType: string; count: number }>;
  stats: {
    peakHour: string;
    averageStay: string;
    totalRevenue: number;
    nftsMinted: number;
  };
}

export const useAnalyticsData = () => {
  return useQuery<AnalyticsData>({
    queryKey: ["analytics"],
    queryFn: async () => {
      const response = await api.get("/analytics");
      return response.data;
    },
    refetchInterval: 300000, // Refresh every 5 minutes
    staleTime: 300000
  });
};