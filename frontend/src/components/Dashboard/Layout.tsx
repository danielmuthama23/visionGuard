import { ReactNode } from 'react'
import Header from '../Shared/Header'
import Sidebar from '../Shared/Sidebar'

interface DashboardLayoutProps {
  children: ReactNode
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <div className="flex">
        <Sidebar />
        
        <main className="flex-1 p-8">
          <div className="max-w-7xl mx-auto space-y-8">
            {/* Overview Section */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="bg-white p-6 rounded-xl shadow-lg">
                <h3 className="text-lg font-semibold">Total Vehicles</h3>
                <p className="text-3xl font-bold mt-2">1,234</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-lg">
                <h3 className="text-lg font-semibold">Current Revenue</h3>
                <p className="text-3xl font-bold mt-2">$12,345</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-lg">
                <h3 className="text-lg font-semibold">Active NFTs</h3>
                <p className="text-3xl font-bold mt-2">892</p>
              </div>
            </div>

            {/* Main Content */}
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}