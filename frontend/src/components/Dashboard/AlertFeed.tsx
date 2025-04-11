import { Alert } from '../../../types'

interface AlertFeedProps {
  alerts: Alert[]
}

export default function AlertFeed({ alerts }: AlertFeedProps) {
  return (
    <div className="h-96 w-full bg-white p-4 rounded-xl shadow-lg overflow-y-auto">
      <h3 className="text-lg font-semibold mb-4">Recent Alerts</h3>
      <div className="space-y-3">
        {alerts.map((alert, index) => (
          <div
            key={index}
            className={`p-3 rounded-lg border-l-4 ${
              alert.severity === 'critical' ? 'border-red-500 bg-red-50' :
              alert.severity === 'warning' ? 'border-yellow-500 bg-yellow-50' :
              'border-blue-500 bg-blue-50'
            }`}
          >
            <div className="flex justify-between items-start">
              <div>
                <p className="font-medium text-sm">{alert.message}</p>
                <p className="text-xs text-gray-500 mt-1">
                  {new Date(alert.timestamp).toLocaleTimeString()}
                </p>
              </div>
              <span className={`text-xs px-2 py-1 rounded-full ${
                alert.severity === 'critical' ? 'bg-red-100 text-red-700' :
                alert.severity === 'warning' ? 'bg-yellow-100 text-yellow-700' :
                'bg-blue-100 text-blue-700'
              }`}>
                {alert.type}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}