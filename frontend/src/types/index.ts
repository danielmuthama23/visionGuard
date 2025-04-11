export interface ParkingLot {
  id: string
  name: string
  location: string
  capacity: number
  currentOccupancy: number
  hourlyRate: number
}

export interface NFTParkingTicket {
  id: string
  plateNumber: string
  entryTime: Date
  exitTime: Date | null
  amountPaid: number
  transactionHash: string
}

export interface Alert {
  id: string
  type: 'capacity' | 'security' | 'payment'
  severity: 'low' | 'medium' | 'high'
  message: string
  timestamp: Date
  resolved: boolean
}

export interface ParkingHistoryEntry {
  id: string
  date: Date
  duration: number
  location: string
  amount: number
  nftId: string
}