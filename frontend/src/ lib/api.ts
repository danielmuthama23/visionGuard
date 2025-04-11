import axios, { AxiosInstance, AxiosRequestConfig } from 'axios'

const apiClient: AxiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for auth token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const api = {
  // Parking operations
  processParkingEntry: (data: FormData) => 
    apiClient.post('/parking/entry', data),
  
  getParkingLots: () => 
    apiClient.get<ParkingLot[]>('/parking'),
  
  // NFT operations
  getNFTs: (accountId: string) => 
    apiClient.get<NFTParkingTicket[]>(`/nfts/${accountId}`),
  
  verifyNFT: (nftId: string) => 
    apiClient.post('/nfts/verify', { nftId }),
  
  // User operations
  login: (credentials: { accountId: string; privateKey: string }) => 
    apiClient.post('/auth/login', credentials),
  
  getParkingHistory: () => 
    apiClient.get<ParkingHistoryEntry[]>('/user/history'),
}

// Type declarations
interface ParkingLot {
  id: string
  name: string
  capacity: number
  available: number
  rate: number
}

interface NFTParkingTicket {
  id: string
  plate: string
  entry: string
  exit?: string
  fee: number
  txHash: string
}

interface ParkingHistoryEntry {
  id: string
  date: string
  duration: number
  fee: number
  nftId: string
}