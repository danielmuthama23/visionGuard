import { useQuery } from "@tanstack/react-query";
import { fetchParkingData } from "@/services/api";

interface ParkingLot {
  id: string;
  name: string;
  capacity: number;
  current: number;
  status: "open" | "closed" | "full";
}

export const useParkingData = () => {
  return useQuery<ParkingLot[], Error>({
    queryKey: ["parkingData"],
    queryFn: async () => {
      try {
        const data = await fetchParkingData();
        return data.map((lot: any) => ({
          id: lot.id,
          name: lot.name,
          capacity: lot.capacity,
          current: lot.current,
          status: lot.current >= lot.capacity ? "full" : 
                 lot.status === "maintenance" ? "closed" : "open"
        }));
      } catch (error) {
        throw new Error("Failed to fetch parking data");
      }
    },
    refetchInterval: 15000, // Refresh every 15 seconds
    staleTime: 10000
  });
};