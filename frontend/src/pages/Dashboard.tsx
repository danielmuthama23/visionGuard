import { ParkingLotCard, LiveFeed, AlertBanner } from "@/components";
import { useParkingData } from "@/hooks/useParkingData";

export const Dashboard = () => {
  const { data, error, isLoading } = useParkingData();
  
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-foreground">Parking Overview</h1>
        <div className="flex gap-2">
          <span className="text-sm text-muted-foreground">
            Last updated: {new Date().toLocaleTimeString()}
          </span>
        </div>
      </div>

      {error && (
        <AlertBanner 
          severity="error" 
          message="Failed to load parking data" 
        />
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {isLoading ? (
          Array(6).fill(0).map((_, i) => (
            <div 
              key={i}
              className="h-32 bg-muted/50 rounded-xl animate-pulse"
            />
          ))
        ) : data?.map((lot) => (
          <ParkingLotCard
            key={lot.id}
            name={lot.name}
            capacity={lot.capacity}
            current={lot.current}
            status={lot.status}
          />
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <LiveFeed />
        <div className="border rounded-xl p-6 bg-background">
          <h2 className="text-lg font-semibold mb-4 text-foreground">
            System Health
          </h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-muted-foreground">Blockchain Status</span>
              <span className="text-green-500">● Connected</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-muted-foreground">AI Processing</span>
              <span className="text-green-500">● Operational</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};