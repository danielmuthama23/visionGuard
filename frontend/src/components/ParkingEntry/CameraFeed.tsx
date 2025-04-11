import { useRef, useState, useEffect } from 'react'
import { useMutation } from 'react-query'
import { processParkingEntry } from '../../../lib/api'
import LoadingSpinner from '../Shared/LoadingSpinner'

interface ScanResult {
  plate: string
  vehicleType: string
  color: string
  fee: number
  nftId: string
}

export default function CameraFeed() {
  const videoRef = useRef<HTMLVideoElement>(null)
  const [scanResult, setScanResult] = useState<ScanResult | null>(null)
  const [cameraError, setCameraError] = useState<string>('')

  const { mutate, isLoading, isError } = useMutation(processParkingEntry, {
    onSuccess: (data) => setScanResult(data),
    onError: () => setCameraError('Failed to process image')
  })

  // Initialize camera
  useEffect(() => {
    const initCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: 'environment' }
        })
        if (videoRef.current) videoRef.current.srcObject = stream
      } catch (err) {
        setCameraError('Camera access required for license plate scanning')
      }
    }
    initCamera()
  }, [])

  const captureFrame = async () => {
    const canvas = document.createElement('canvas')
    const video = videoRef.current!
    
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    const ctx = canvas.getContext('2d')!
    ctx.drawImage(video, 0, 0)
    
    canvas.toBlob(blob => {
      if (blob) {
        const formData = new FormData()
        formData.append('image', blob)
        mutate(formData)
      }
    }, 'image/jpeg')
  }

  return (
    <div className="camera-container">
      {cameraError ? (
        <div className="camera-error">{cameraError}</div>
      ) : (
        <>
          <video ref={videoRef} autoPlay playsInline className="camera-feed" />
          <button 
            onClick={captureFrame}
            disabled={isLoading}
            className="capture-button"
          >
            {isLoading ? <LoadingSpinner /> : 'Scan License Plate'}
          </button>
        </>
      )}

      {isError && (
        <div className="error-message">
          Failed to process image. Please try again.
        </div>
      )}

      {scanResult && <NFTConfirmation {...scanResult} />}
    </div>
  )
}