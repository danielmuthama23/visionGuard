import { useEffect } from 'react'
import { useRouter } from 'next/router'
import { useHederaWallet } from '../../../lib/hedera'

interface AuthGuardProps {
  children: React.ReactNode
}

export default function AuthGuard({ children }: AuthGuardProps) {
  const router = useRouter()
  const { accountId, isLoading } = useHederaWallet()

  useEffect(() => {
    if (!isLoading && !accountId) {
      router.push('/login')
    }
  }, [accountId, isLoading, router])

  if (isLoading || !accountId) {
    return <div className="loading-screen">Loading wallet...</div>
  }

  return <>{children}</>
}