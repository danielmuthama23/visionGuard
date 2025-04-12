import { NFTBadge } from "@/components";
import { useNFTData } from "@/hooks/useNFTData";
import { NFT, NFTResponse } from "@/types/types";
import { formatDate } from "@/lib/utils";

export const NFTViewer = () => {
  const { data, isLoading } = useNFTData();
  const nftData = data as NFTResponse;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-foreground">NFT Management</h1>
        <button className="primary-btn">
          Refresh NFTs
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {isLoading ? (
          Array(6).fill(0).map((_, i) => (
            <div 
              key={i}
              className="h-48 bg-muted/50 rounded-xl animate-pulse"
            />
          ))
        ) : nftData?.nfts?.map((nft: NFT) => (
          <div
            key={nft.id}
            className="group relative bg-background rounded-xl border p-6 hover:border-primary/20 transition-colors"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-semibold text-foreground">
                #{nft.id.slice(0, 8)}
              </h3>
              <NFTBadge nftId={nft.id} />
            </div>
            
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Vehicle</span>
                <span className="text-foreground">
                  {nft.vehicleType} • {nft.color}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Duration</span>
                <span className="text-foreground">
                  {nft.duration} hours
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Minted</span>
                <span className="text-foreground">
                  {formatDate(nft.timestamp)}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};