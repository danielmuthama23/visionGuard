import { useEffect, useState } from 'react'
import { useSWRConfig } from 'swr'

type RealtimeEvent = 
  | { type: 'capacity'; lotId: string; capacity: number }
  | { type: 'alert'; message: string; severity: 'info' | 'warning' | 'critical' }
  | { type: 'nft'; accountId: string }

export const useRealtime = () => {
  const [socket, setSocket] = useState<WebSocket | null>(null)
  const { mutate } = useSWRConfig()

  useEffect(() => {
    const ws = new WebSocket(process.env.NEXT_PUBLIC_WS_URL!)
    
    ws.onopen = () => {
      console.log('WebSocket connected')
      setSocket(ws)
    }

    ws.onmessage = (event) => {
      const data: RealtimeEvent = JSON.parse(event.data)
      
      switch(data.type) {
        case 'capacity':
          mutate(`/api/parking/${data.lotId}`)
          break
          
        case 'alert':
          mutate('/api/alerts', (prev: Alert[]) => [data, ...(prev || [])])
          break
          
        case 'nft':
          mutate(`/api/nfts/${data.accountId}`)
          break
      }
    }

    return () => {
      ws.close()
      setSocket(null)
    }
  }, [mutate])

  return {
    sendEvent: (event: RealtimeEvent) => {
      socket?.send(JSON.stringify(event))
    }
  }
}