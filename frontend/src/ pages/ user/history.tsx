import useSWR from 'swr'
import ParkingHistoryTable from '../../../components/User/ParkingHistoryTable'
import DashboardLayout from '../../../components/Dashboard/Layout'

export default function HistoryPage() {
  const { data: history, error } = useSWR('/api/user/history')

  return (
    <DashboardLayout>
      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold mb-6">Parking History</h1>
        
        {error && <div className="text-red-500">Error loading history</div>}
        {!history && <div>Loading history...</div>}
        
        <ParkingHistoryTable entries={history || []} />
      </div>
    </DashboardLayout>
  )
}