// src/types/index.ts

export interface WebSocketEvent {
    eventType: 'vehicle_entry' | 'vehicle_exit' | 'system_alert';
    timestamp: string;
    data: {
      lotId: string;
      licensePlate?: string;
      vehicleType?: string;
      message?: string;
      nftId?: string;
    };
  }

  export interface ParkingLot {
    id: string;
    name: string;
    capacity: number;
    current: number;
    status: 'open' | 'closed' | 'full';
  }

  export interface AnalyticsData {
    hourlyData: HourlyData[];
    dailyTrends: DailyTrend[];
    stats: AnalyticsStats;
  }
  
  interface HourlyData {
    hour: string;
    count: number;
  }
  
  interface DailyTrend {
    day: string;
    vehicleType: string;
    count: number;
  }
  
  interface AnalyticsStats {
    peakHour: string;
    averageStay: string;
    totalRevenue: number;
    nftsMinted: number;
  }