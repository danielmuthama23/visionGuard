import { useEffect, useState } from 'react';
import { NFTBadge } from './NFTBadge';
import { Skeleton } from './ui/skeleton';

interface LiveFeedEntry {
  id: string;
  plate: string;
  vehicleType: string;
  timestamp: Date;
  nftId?: string;
}

export const LiveFeed = () => {
  const [entries, setEntries] = useState<LiveFeedEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate WebSocket connection
    const ws = new WebSocket('wss://api.visionguard.io/live');
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setEntries(prev => [data, ...prev.slice(0, 9)]);
      setLoading(false);
    };

    return () => ws.close();
  }, []);

  return (
    <div className="border rounded-xl bg-background p-6">
      <h2 className="text-lg font-semibold mb-4 text-foreground">
        Real-time Activity
      </h2>
      
      <div className="space-y-4">
        {loading ? (
          Array(5).fill(0).map((_, i) => (
            <Skeleton key={i} className="h-16 w-full rounded-lg" />
          ))
        ) : entries.map((entry) => (
          <div
            key={entry.id}
            className="flex items-center gap-4 p-4 bg-muted/50 rounded-lg animate-in fade-in"
          >
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <span className="font-medium text-foreground">
                  {entry.plate}
                </span>
                {entry.nftId && <NFTBadge nftId={entry.nftId} />}
              </div>
              <div className="text-sm text-muted-foreground">
                {entry.vehicleType} •{' '}
                {new Date(entry.timestamp).toLocaleTimeString()}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};