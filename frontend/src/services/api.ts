// src/services/api.ts
import { useQuery } from "@tanstack/react-query";
import axios, { type AxiosError, type AxiosInstance, type AxiosResponse } from "axios";

// Update the ParkingLot interface to match the API response
export interface ParkingLot {
  id: string;
  name: string;
  capacity: number;
  current: number;
  status: "open" | "closed" | "full" | "maintenance"; // Add 'maintenance' to the union type
}

// Environment variable types should be in vite-env.d.ts
interface ImportMetaEnv {
  readonly VITE_API_URL: string;
  readonly VITE_API_TOKEN: string;
}

const createApiClient = (): AxiosInstance => {
  if (!import.meta.env.VITE_API_URL || !import.meta.env.VITE_API_TOKEN) {
    throw new Error("Missing required environment variables");
  }

  return axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${import.meta.env.VITE_API_TOKEN}`
    }
  });
};

export const api = createApiClient();

export const fetchParkingData = async (): Promise<ParkingLot[]> => {
  try {
    const response: AxiosResponse<ParkingLot[]> = await api.get("/parking");
    return response.data;
  } catch (error) {
    const axiosError = error as AxiosError;
    console.error("Parking data fetch error:", axiosError.toJSON());
    throw new Error(`Parking data fetch failed: ${axiosError.message}`);
  }
};

export const useParkingData = () => {
  return useQuery<ParkingLot[], Error>({
    queryKey: ["parkingData"],
    queryFn: async () => {
      try {
        const data = await fetchParkingData();
        return data.map((lot) => ({
          ...lot,
          status: lot.current >= lot.capacity ? "full" : 
                 lot.status === "maintenance" ? "closed" : lot.status
        }));
      } catch (error) {
        if (axios.isAxiosError(error)) {
          throw new Error(error.response?.data?.message || error.message);
        }
        throw new Error("Failed to fetch parking data");
      }
    },
    refetchInterval: 15000,
    staleTime: 10000
  });
};