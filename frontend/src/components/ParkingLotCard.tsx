import { cn } from "@/lib/utils";

interface ParkingLotCardProps {
  name: string;
  capacity: number;
  current: number;
  status: 'open' | 'closed' | 'full';
  className?: string;
}

export const ParkingLotCard = ({
  name,
  capacity,
  current,
  status,
  className
}: ParkingLotCardProps) => {
  const percentage = Math.round((current / capacity) * 100);
  
  return (
    <div className={cn(
      "group relative bg-background rounded-xl p-6 shadow-sm transition-all",
      "hover:shadow-md border hover:border-primary/20",
      className
    )}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-foreground">{name}</h3>
        <span className={cn(
          "inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium",
          status === 'open' && 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400',
          status === 'full' && 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400',
          status === 'closed' && 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-400'
        )}>
          <span className={cn(
            "w-2 h-2 rounded-full",
            status === 'open' && 'bg-green-500',
            status === 'full' && 'bg-red-500',
            status === 'closed' && 'bg-gray-500'
          )} />
          {status.charAt(0).toUpperCase() + status.slice(1)}
        </span>
      </div>
      
      <div className="space-y-4">
        <div className="flex justify-between text-sm">
          <span className="text-muted-foreground">Occupancy</span>
          <span className="font-medium text-foreground">
            {current}/{capacity} ({percentage}%)
          </span>
        </div>
        
        <div className="relative h-2.5 rounded-full bg-gray-100 dark:bg-gray-800 overflow-hidden">
          <div 
            className="absolute left-0 top-0 h-full bg-primary transition-all duration-500"
            style={{ width: `${percentage}%` }}
          />
        </div>
      </div>
    </div>
  );
};