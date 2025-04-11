import Link from 'next/link'
import { useHederaWallet } from '../../../lib/hedera'

export default function Header() {
  const { accountId, connectWallet, disconnect } = useHederaWallet()

  return (
    <header className="header">
      <nav className="nav-container">
        <Link href="/" className="logo">
          VisionGuard
        </Link>
        
        <div className="nav-links">
          <Link href="/dashboard" className="nav-link">
            Dashboard
          </Link>
          <Link href="/history" className="nav-link">
            History
          </Link>
        </div>

        <div className="wallet-section">
          {accountId ? (
            <>
              <span className="account-id">
                {accountId.slice(0, 6)}...{accountId.slice(-4)}
              </span>
              <button onClick={disconnect} className="wallet-button">
                Disconnect
              </button>
            </>
          ) : (
            <button onClick={connectWallet} className="wallet-button">
              Connect Wallet
            </button>
          )}
        </div>
      </nav>
    </header>
  )
}