import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { ParkingHistory } from '../../../types'

interface CapacityChartProps {
  data: ParkingHistory[]
}

export default function CapacityChart({ data }: CapacityChartProps) {
  return (
    <div className="h-80 w-full bg-white p-4 rounded-xl shadow-lg">
      <h3 className="text-lg font-semibold mb-4">Hourly Capacity Trends</h3>
      <ResponsiveContainer width="100%" height="90%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="hour"
            tickFormatter={(hour) => `${hour}:00`}
          />
          <YAxis domain={[0, 100]} />
          <Tooltip
            contentStyle={{ background: '#fff', border: 'none', borderRadius: '8px' }}
            formatter={(value) => [`${value}%`, 'Capacity']}
          />
          <Line
            type="monotone"
            dataKey="capacity"
            stroke="#3b82f6"
            strokeWidth={2}
            dot={{ r: 4 }}
            activeDot={{ r: 8 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}