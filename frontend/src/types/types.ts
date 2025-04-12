// export interface ParkingLot {
//   id: string;
//   name: string;
//   capacity: number;
//   current: number;
//   status: "open" | "closed" | "full" | "maintenance"
//   location: string;
// }

// src/types/types.ts
export interface ParkingLot {
  id: string;
  name: string;
  capacity: number;
  current: number;
  status: "open" | "closed" | "full" | "maintenance";
}

export type ParkingStatus = ParkingLot["status"];  // Helper type

export interface NFT {
  id: string;
  plate: string;
  mintDate: Date;
  vehicleType: string;
  color: string;
  imageUrl?: string;
}

export type AlertSeverity = 'info' | 'success' | 'warning' | 'error';

export interface WebSocketEvent {
  type: 'entry' | 'exit';
  plate: string;
  timestamp: string;
  lotId: string;
  nftId?: string;
}

// src/types/types.ts
export interface NFT {
  id: string;
  plate: string;
  vehicleType: string;
  color: string;
  duration: number;
  timestamp: string;  // ISO date string
  imageUrl?: string;
}

export interface NFTResponse {
  nfts: NFT[];
  total: number;
}

export interface AnalyticsData {
  hourlyData: Array<{
    hour: string;
    count: number;
  }>;
  dailyTrends: Array<{
    vehicleType: string;
    count: number;
  }>;
  stats: {
    peakHour: string;
    averageStay: string;
    totalRevenue: number;
    nftsMinted: number;
  };
}