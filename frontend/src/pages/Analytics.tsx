import { InsightChart } from "@/components";
import { useAnalyticsData } from "@/hooks/useAnalyticsData";


export const Analytics = () => {
    const { data, isLoading } = useAnalyticsData();
  
    // Transform data to match InsightChart's expected format
    const hourlyChartData = (data?.hourlyData || []).map(({ hour, count }) => ({
      name: hour,
      value: count
    }));
  
    const vehicleTypeData = (data?.dailyTrends || []).map(({ vehicleType, count }) => ({
      name: vehicleType,
      value: count
    }));
  
    return (
      <div className="space-y-8">
        <h1 className="text-3xl font-bold text-foreground">Parking Analytics</h1>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="p-6 bg-background rounded-xl border">
            <h2 className="text-lg font-semibold mb-4">Hourly Occupancy</h2>
            <InsightChart 
              data={hourlyChartData}
              type="line"
              color="#2563eb"
            />
          </div>
          
          <div className="p-6 bg-background rounded-xl border">
            <h2 className="text-lg font-semibold mb-4">Vehicle Type Distribution</h2>
            <InsightChart
              data={vehicleTypeData}
              type="bar"
              color="#4f46e5"
            />
          </div>
        </div>
  
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="p-6 bg-background rounded-xl border">
          <div className="text-muted-foreground">Peak Hour</div>
          <div className="text-2xl font-bold mt-2">
            {isLoading ? '--:--' : data?.stats.peakHour || '08:30 AM'}
          </div>
        </div>
        <div className="p-6 bg-background rounded-xl border">
          <div className="text-muted-foreground">Avg. Stay Duration</div>
          <div className="text-2xl font-bold mt-2">
            {isLoading ? '--h --m' : data?.stats.averageStay || '2h 15m'}
          </div>
        </div>
        <div className="p-6 bg-background rounded-xl border">
          <div className="text-muted-foreground">Total Revenue</div>
          <div className="text-2xl font-bold mt-2">
            ${isLoading ? '---' : data?.stats.totalRevenue?.toLocaleString() || '12,450'}
          </div>
        </div>
        <div className="p-6 bg-background rounded-xl border">
          <div className="text-muted-foreground">NFTs Minted</div>
          <div className="text-2xl font-bold mt-2">
            {isLoading ? '---' : data?.stats.nftsMinted?.toLocaleString() || '1,234'}
          </div>
        </div>
      </div>
    </div>
  );
};

