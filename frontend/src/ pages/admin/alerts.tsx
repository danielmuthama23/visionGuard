import { useState } from 'react'
import AlertTable from '../../../components/Admin/AlertTable'
import DashboardLayout from '../../../components/Dashboard/Layout'

export default function AlertsPage() {
  const [alertConfig, setAlertConfig] = useState({
    capacityThreshold: 90,
    notifyEmail: true,
    notifySMS: false
  })

  return (
    <DashboardLayout>
      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold mb-6">Alert Configuration</h1>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <AlertTable />
          
          <div className="bg-white p-6 rounded-xl shadow-lg">
            <h2 className="text-xl font-semibold mb-4">Notification Settings</h2>
            <form className="space-y-4">
              <div className="form-group">
                <label>Capacity Threshold (%)</label>
                <input
                  type="number"
                  value={alertConfig.capacityThreshold}
                  onChange={(e) => setAlertConfig({...alertConfig, capacityThreshold: Number(e.target.value)})}
                />
              </div>
              <div className="form-group">
                <label>
                  <input
                    type="checkbox"
                    checked={alertConfig.notifyEmail}
                    onChange={(e) => setAlertConfig({...alertConfig, notifyEmail: e.target.checked})}
                  />
                  Email Notifications
                </label>
              </div>
              {/* Additional settings */}
            </form>
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}