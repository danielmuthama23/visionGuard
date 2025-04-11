import { useState } from 'react'
import { HederaWallet } from '../../../lib/hedera'
import { completeParkingEntry } from '../../../lib/api'

interface NFTConfirmationProps {
  plate: string
  vehicleType: string
  color: string
  fee: number
  nftId: string
}

export default function NFTConfirmation({ 
  plate, 
  vehicleType, 
  color, 
  fee, 
  nftId 
}: NFTConfirmationProps) {
  const [paymentStatus, setPaymentStatus] = useState<'idle' | 'processing' | 'success'>('idle')
  const [wallet] = useState(() => new HederaWallet())

  const handlePayment = async () => {
    setPaymentStatus('processing')
    try {
      // 1. Send payment transaction
      await wallet.sendPayment(nftId, fee)
      
      // 2. Confirm entry with backend
      await completeParkingEntry(nftId)
      
      setPaymentStatus('success')
    } catch (error) {
      setPaymentStatus('idle')
    }
  }

  return (
    <div className="nft-confirmation">
      <h3>Confirm Parking Details</h3>
      
      <div className="vehicle-details">
        <p><span>License Plate:</span> {plate}</p>
        <p><span>Vehicle Type:</span> {vehicleType}</p>
        <p><span>Color:</span> {color}</p>
        <p><span>Fee:</span> {fee} HBAR</p>
      </div>

      <button
        onClick={handlePayment}
        disabled={paymentStatus !== 'idle'}
        className="confirm-button"
      >
        {paymentStatus === 'processing' 
          ? 'Processing Payment...' 
          : 'Confirm with NFT Payment'}
      </button>

      {paymentStatus === 'success' && (
        <div className="success-message">
          ✅ Payment confirmed! Your NFT parking pass has been minted.
          <a 
            href={`https://hashscan.io/testnet/token/${nftId}`}
            target="_blank"
            rel="noopener noreferrer"
          >
            View Transaction
          </a>
        </div>
      )}
    </div>
  )
}