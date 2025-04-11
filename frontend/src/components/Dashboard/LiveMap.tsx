import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import L from 'leaflet'
import { ParkingLot } from '../../types'

interface LiveMapProps {
  lots: ParkingLot[]
}

const parkingIcon = (capacity: number) => L.divIcon({
  className: `parking-marker ${capacity > 90 ? 'full' : capacity > 75 ? 'busy' : 'available'}`,
  html: `<div>${capacity}%</div>`
})

export default function LiveMap({ lots }: LiveMapProps) {
  return (
    <MapContainer center={[51.505, -0.09]} zoom={13} className="h-full">
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/>
      
      {lots.map(lot => (
        <Marker key={lot.id} position={[lot.lat, lot.lng]} icon={parkingIcon(lot.capacity)}>
          <Popup>
            <h3>{lot.name}</h3>
            <p>Capacity: {lot.capacity}%</p>
            <p>Available: {lot.availableSpaces}</p>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  )
}