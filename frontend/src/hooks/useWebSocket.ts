import { useEffect, useState } from "react";
import { WebSocketEvent } from "@/types";

export const useWebSocket = (url: string) => {
  const [data, setData] = useState<WebSocketEvent[]>([]);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const ws = new WebSocket(url);
    let reconnectInterval: NodeJS.Timeout;

    const handleReconnect = () => {
      reconnectInterval = setInterval(() => {
        new WebSocket(url);
      }, 5000);
    };

    ws.onopen = () => {
      console.log("WebSocket connected");
      setError(null);
      clearInterval(reconnectInterval);
    };

    ws.onmessage = (event) => {
      const newData: WebSocketEvent = JSON.parse(event.data);
      setData(prev => [newData, ...prev.slice(0, 49)]); // Keep last 50 entries
    };

    ws.onerror = (err) => {
      setError(new Error("WebSocket connection error"));
      handleReconnect();
    };

    ws.onclose = () => {
      setError(new Error("WebSocket disconnected"));
      handleReconnect();
    };

    return () => {
      ws.close();
      clearInterval(reconnectInterval);
    };
  }, [url]);

  return { data, error };
};