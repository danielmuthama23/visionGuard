import Link from 'next/link'
import { useHederaWallet } from '../lib/hedera'

export default function HomePage() {
  const { connectWallet } = useHederaWallet()

  return (
    <div className="min-h-screen bg-gray-50">
      <main className="max-w-7xl mx-auto px-4 py-16 text-center">
        <h1 className="text-5xl font-bold mb-8">VisionGuard Parking</h1>
        <p className="text-xl text-gray-600 mb-12">
          Smart Parking Management Powered by AI and Blockchain
        </p>
        
        <div className="flex justify-center gap-4 mb-16">
          <button 
            onClick={connectWallet}
            className="cta-button"
          >
            Get Started
          </button>
          <Link href="/dashboard" className="cta-button secondary">
            View Demo
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <FeatureCard
            title="AI-Powered Monitoring"
            description="Real-time vehicle detection and license plate recognition"
          />
          <FeatureCard
            title="Blockchain Payments"
            description="Secure NFT-based parking transactions"
          />
          <FeatureCard
            title="Smart Alerts"
            description="Instant notifications for capacity and security events"
          />
        </div>
      </main>
    </div>
  )
}

const FeatureCard = ({ title, description }: { title: string, description: string }) => (
  <div className="bg-white p-6 rounded-xl shadow-lg">
    <h3 className="text-xl font-semibold mb-3">{title}</h3>
    <p className="text-gray-600">{description}</p>
  </div>
)