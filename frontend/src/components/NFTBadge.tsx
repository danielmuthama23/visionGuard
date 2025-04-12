import { cn } from "@/lib/utils";
import { IoSparkles } from 'react-icons/io5';

interface NFTBadgeProps {
  nftId: string;
  className?: string;
}

export const NFTBadge = ({ nftId, className }: NFTBadgeProps) => {
  return (
    <div
      className={cn(
        "inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs",
        "bg-purple-100 text-purple-800 dark:bg-purple-900/20 dark:text-purple-300",
        "transition-colors hover:bg-purple-200/80 cursor-pointer",
        className
      )}
      onClick={() => console.log('View NFT:', nftId)} // Replace with actual handler
    >
      <IoSparkles className="w-3.5 h-3.5" />
      <span>NFT Verified</span>
    </div>
  );
};