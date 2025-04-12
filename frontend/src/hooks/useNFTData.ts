import { useQuery } from "@tanstack/react-query";
import { api } from "@/services/api";
import { NFTResponse } from "@/types/types";

export const useNFTData = () => {
  return useQuery<NFTResponse>({
    queryKey: ["nfts"],
    queryFn: async () => {
      const response = await api.get("/nfts");
      return response.data;
    }
  });
};